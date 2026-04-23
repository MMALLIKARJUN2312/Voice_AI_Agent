from scheduler.appointment_engine.engine import book_appointment

def route_tool(action):
    tool = action.get("tool")
    args = action.get("arguments", {})

    if tool == "book_appointment":
        args.setdefault("doctor", "general")
        args.setdefault("date", "tomorrow")
        args.setdefault("time", "10:00")

        return book_appointment(args)

    return {"message": "Invalid tool"}