import google.generativeai as genai
import os
import json
from agent.prompt.system_prompt import SYSTEM_PROMPT
from agent.tools.tool_router import route_tool

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def run_agent(text, lang):

    prompt = f"{SYSTEM_PROMPT}\nUser: {text}"

    response = model.generate_content(prompt)

    try:
        parsed = json.loads(response.text)
        result = route_tool(parsed)

        return {
            "response": result.get("message"),
            "trace": parsed
        }

    except:
        return {
            "response": "Sorry, I couldn't understand that.",
            "trace": response.text
        }