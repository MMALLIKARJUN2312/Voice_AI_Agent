import time
from loguru import logger

from services.speech_to_text.stt import transcribe
from services.language_detection.detect import detect_language
from agent.reasoning.agent_engine import run_agent
from services.text_to_speech.tts import synthesize


async def process_voice(payload: dict) -> dict:
    start_time = time.time()

    try:
        audio = payload.get("audio")
        if not audio:
            raise ValueError("No audio provided in payload")

        logger.info("Starting voice processing pipeline")

        t1 = time.time()
        text = transcribe(audio)
        logger.info(f"STT completed in {(time.time() - t1) * 1000:.2f} ms")

        t2 = time.time()
        lang = detect_language(text)
        logger.info(f"Language detected: {lang} in {(time.time() - t2) * 1000:.2f} ms")

        t3 = time.time()
        agent_output = run_agent(text, lang)
        logger.info(f"Agent response generated in {(time.time() - t3) * 1000:.2f} ms")

        t4 = time.time()
        audio_response = synthesize(agent_output.get("response", ""), lang)
        logger.info(f"TTS completed in {(time.time() - t4) * 1000:.2f} ms")

        total_latency = round((time.time() - start_time) * 1000, 2)
        logger.info(f"Total pipeline latency: {total_latency} ms")

        return {
            "text": agent_output,
            "audio": audio_response,
            "latency_ms": total_latency
        }

    except Exception as e:
        logger.exception("Error in voice processing pipeline")

        return {
            "error": str(e),
            "latency_ms": round((time.time() - start_time) * 1000, 2)
        }