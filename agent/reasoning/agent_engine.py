import google.generativeai as genai
import json
import os
import re
import time
from dotenv import load_dotenv
from agent.tools.tool_router import route_tool
from loguru import logger

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

def extract_json(text: str):
    if not text:
        return None

    try:
        return json.loads(text)
    except:
        pass

    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception as e:
        logger.error(f"JSON extraction failed: {e}")

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

    if "cancel" in text:
        return {
            "tool": "cancel_appointment",
            "arguments": {}
        }

    if "reschedule" in text:
        return {
            "tool": "reschedule_appointment",
            "arguments": {}
        }

    return None

def validate_action(parsed):
    if not isinstance(parsed, dict):
        return False

    if "tool" not in parsed:
        return False

    if "arguments" not in parsed:
        parsed["arguments"] = {}

    return True


def run_agent(text, context):
    start_time = time.time()

    prompt = f"""
You are a strict JSON API.

Return ONLY valid JSON. No explanation. No markdown.

Schema:
{{
  "tool": "book_appointment | cancel_appointment | reschedule_appointment | check_availability",
  "arguments": {{
    "doctor": "string",
    "date": "string",
    "time": "string"
  }}
}}

User: {text}
"""

    try:
        response = model.generate_content(prompt)

        raw_output = response.text
        logger.info(f"Gemini raw output: {raw_output}")

        parsed = extract_json(raw_output)

        if not parsed:
            logger.warning("⚠️ LLM JSON parsing failed → using fallback parser")
            parsed = fallback_parser(text)

        if not parsed:
            return {
                "response": "Sorry, I couldn't understand that."
            }

        if not validate_action(parsed):
            logger.error(f"Invalid action format: {parsed}")
            return {
                "response": "Invalid request format from AI"
            }

        try:
            tool_result = route_tool(parsed)
        except Exception as tool_error:
            logger.error(f"Tool execution failed: {tool_error}")
            return {
                "response": "Error executing action"
            }

        latency = round((time.time() - start_time) * 1000, 2)

        return {
            "response": tool_result.get("message", "Done"),
            "trace": parsed,
            "agent_latency_ms": latency
        }

    except Exception as e:
        logger.exception(f"🔥 AGENT FAILURE: {e}")

        return {
            "response": "System error occurred"
        }