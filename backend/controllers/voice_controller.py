import time
from services.speech_to_text.stt import transcribe
from services.language_detection.detect import detect_language
from agent.reasoning.agent_engine import run_agent
from services.text_to_speech.tts import synthesize

async def process_voice(payload):
    start = time.time()

    audio = payload.get("audio")

    text = transcribe(audio)
    lang = detect_language(text)

    agent_output = run_agent(text, lang)

    audio_response = synthesize(agent_output["response"], lang)

    latency = round((time.time() - start) * 1000, 2)

    return {
        "text": agent_output,
        "audio": audio_response,
        "latency_ms": latency
    }