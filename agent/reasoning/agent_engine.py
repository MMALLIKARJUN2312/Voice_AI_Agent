import google.generativeai as genai
import json
import os
import re
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt
from agent.tools.tool_router import route_tool
from loguru import logger

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def extract_json(text: str):
    try:
        return json.loads(text)
    except:
        pass

    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass

    return None


def fallback_parser(text: str):
    text = text.lower()

    if "book" in text:
        return {
            "tool": "book_appointment",
            "arguments": {
                "doctor": "general",
                "date": "tomorrow",
                "time": "10:00"
            }
        }

    return None


@retry(stop=stop_after_attempt(2)) 
def run_agent(text, context):

    prompt = f"""
You are a strict JSON API.

Return ONLY JSON. No text.

{{
  "tool": "",
  "arguments": {{
    "doctor": "",
    "date": "",
    "time": ""
  }}
}}

User: {text}
"""

    try:
        response = model.generate_content(prompt)
        raw = response.text

        parsed = extract_json(raw)

        if not parsed:
            logger.warning("LLM JSON failed, using fallback")
            parsed = fallback_parser(text)

        if not parsed:
            return {"response": "Sorry, I couldn't understand that."}

        result = route_tool(parsed)

        return {
            "response": result.get("message", "Done"),
            "trace": parsed
        }

    except Exception as e:
        logger.error(f"Agent Error: {e}")
        return {"response": "System error occurred"}