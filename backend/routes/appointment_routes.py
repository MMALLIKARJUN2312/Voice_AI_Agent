from fastapi import APIRouter
from scheduler.appointment_engine.engine import book_appointment

router = APIRouter()

@router.post("/book")
def book(data: dict):
    return book_appointment(data)