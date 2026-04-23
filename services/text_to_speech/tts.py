def synthesize(text: str, lang: str = "en") -> str:
    if not text:
        return "[ERROR] Empty response"
    return f"[AUDIO-{lang}] {text}"