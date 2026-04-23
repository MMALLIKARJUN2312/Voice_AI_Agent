from scheduler.appointment_engine.engine import book_appointment

def route_tool(action):
    if action["tool"] == "book_appointment":
        result = book_appointment(action["arguments"])
        return {"message": f"Booked at {result['slot']}"}

    return {"message": "Invalid action"}