import time
from loguru import logger
from services.speech_to_text.stt import transcribe
from services.language_detection.detect import detect_language
from agent.reasoning.agent_engine import run_agent
from services.text_to_speech.tts import synthesize


async def process_voice(payload):
    start = time.time()

    try:
        audio_input = payload.get("audio")

        if isinstance(audio_input, str):
            text = audio_input
        else:
            # Real audio pipeline
            text = transcribe(audio_input)

        lang = detect_language(text)

        agent_output = run_agent(text, lang)

        audio_response = synthesize(agent_output["response"], lang)

        latency = round((time.time() - start) * 1000, 2)

        return {
            "text": agent_output,
            "audio": audio_response,
            "latency_ms": latency
        }

    except Exception as e:
        logger.error(f"Error: {e}")
        return {
            "error": str(e),
            "latency_ms": round((time.time() - start) * 1000, 2)
        }