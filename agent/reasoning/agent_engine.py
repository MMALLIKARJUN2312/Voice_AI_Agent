import google.generativeai as genai
import json
import os
from tenacity import retry, stop_after_attempt
from agent.tools.tool_router import route_tool

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
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

Return JSON:
{{
 "tool": "",
 "arguments": {{}}
}}
"""

    response = model.generate_content(prompt)

    parsed = json.loads(response.text)

    tool_result = route_tool(parsed)

    return {
        "response": tool_result["message"],
        "trace": parsed
    }