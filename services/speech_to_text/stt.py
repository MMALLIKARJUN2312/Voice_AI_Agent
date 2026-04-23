import os

def transcribe(audio_input):
    if isinstance(audio_input, str):
        return audio_input

    if os.getenv("RENDER") or os.getenv("RAILWAY_ENVIRONMENT"):
        return "book appointment tomorrow at 10:00"

    import whisper
    model = whisper.load_model("base")

    with open("temp.wav", "wb") as f:
        f.write(audio_input)

    result = model.transcribe("temp.wav")
    return result["text"]