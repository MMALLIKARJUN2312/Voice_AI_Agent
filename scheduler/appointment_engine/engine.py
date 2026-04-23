from datetime import datetime

def book_appointment(data):

    time = data.get("time", "10:00")

    try:
        parsed_time = datetime.strptime(time, "%H:%M").time()
    except:
        return {"message": "Invalid time format"}

    if parsed_time < datetime.now().time():
        return {"message": "Cannot book past time"}

    return {"message": f"Appointment booked at {time}"}