from fastapi import APIRouter
from backend.controllers.voice_controller import process_voice

router = APIRouter()

@router.post("/process")
async def process(payload: dict):
    return await process_voice(payload)