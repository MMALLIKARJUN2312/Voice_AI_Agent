def check_availability(doctor, date):
    return ["10:00 AM", "2:00 PM", "4:00 PM"]

def book_appointment(data):
    slots = check_availability(data["doctor"], data["date"])

    if not slots:
        return {"error": "No slots available"}

    return {"slot": slots[0]}