import google.generativeai as genai
import json
import os
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, retry_if_exception_type
from agent.tools.tool_router import route_tool
from loguru import logger

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

def clean_json(text: str):
    try:
        text = text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
        return json.loads(text)
    except Exception as e:
        logger.error(f"JSON parse failed: {text}")
        return None

@retry(
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(Exception)
)
def run_agent(text, context):

    prompt = f"""
You are a healthcare assistant.

Available tools:
- book_appointment
- cancel_appointment
- reschedule_appointment
- check_availability

IMPORTANT:
- Always return valid JSON
- Do NOT add explanations

User: {text}

Return STRICT JSON:
{{
 "tool": "",
 "arguments": {{}}
}}
"""

    try:
        response = model.generate_content(prompt)
        raw_output = response.text

        parsed = clean_json(raw_output)

        if not parsed:
            return {"response": "Sorry, I couldn't understand that."}

        if "tool" not in parsed or "arguments" not in parsed:
            return {"response": "Invalid response from AI"}

        try:
            tool_result = route_tool(parsed)
        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            return {"response": "Error executing action"}

        return {
            "response": tool_result.get("message", "Done"),
            "trace": parsed
        }

    except Exception as e:
        logger.error(f"LLM Error: {e}")
        return {
            "response": "I'm having trouble processing that request"
        }