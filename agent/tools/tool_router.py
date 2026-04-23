from scheduler.appointment_engine.engine import (
    book_appointment,
    check_availability
)

def route_tool(action):
    tool = action.get("tool")

    if tool == "book_appointment":
        return book_appointment(action["arguments"])

    if tool == "check_availability":
        return check_availability(**action["arguments"])

    return {"message": "Invalid tool"}