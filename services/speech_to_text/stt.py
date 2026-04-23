import whisper

model = whisper.load_model("base")

def transcribe(audio_bytes):
    with open("temp.wav", "wb") as f:
        f.write(audio_bytes)

    result = model.transcribe("temp.wav")
    return result["text"]