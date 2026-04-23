from fastapi import FastAPI
from backend.routes.voice_routes import router as voice_router
from backend.routes.appointment_routes import router as appointment_router

app = FastAPI(title="Voice AI Agent")

app.include_router(voice_router, prefix="/voice")
app.include_router(appointment_router, prefix="/appointment")

@app.get("/")
def health():
    return {"status": "ok"}