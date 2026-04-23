import google.generativeai as genai
import json
import os
from tenacity import retry, stop_after_attempt
from dotenv import load_dotenv
from agent.tools.tool_router import route_tool

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")


@retry(stop=stop_after_attempt(3))
def run_agent(text, context):

    prompt = f"""
You are a healthcare assistant.

Available tools:
- book_appointment
- cancel_appointment
- reschedule_appointment
- check_availability

User: {text}

Return STRICT JSON:
{{
 "tool": "",
 "arguments": {{}}
}}
"""

    response = model.generate_content(prompt)

    try:
        parsed = json.loads(response.text)
    except:
        return {"response": "I'm having trouble processing that request"}

    tool_result = route_tool(parsed)

    return {
        "response": tool_result["message"],
        "trace": parsed
    }