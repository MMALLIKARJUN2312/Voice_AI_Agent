from datetime import datetime

def validate_slot(slot_time):
    if slot_time < datetime.now().time():
        return False
    return True

def check_availability(doctor, date):
    return {"slots": ["10:00", "14:00"]}

def book_appointment(data):
    slot = data.get("time")

    if not validate_slot(datetime.strptime(slot, "%H:%M").time()):
        return {"message": "Cannot book past time"}

    return {"message": f"Appointment booked at {slot}"}