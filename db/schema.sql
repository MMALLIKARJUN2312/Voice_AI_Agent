CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    patient_id VARCHAR(50),
    doctor_id VARCHAR(50),
    date DATE,
    time TIME,
    status VARCHAR(20)
);

CREATE TABLE doctor_schedule (
    doctor_id VARCHAR(50),
    date DATE,
    slot TIME,
    is_booked BOOLEAN DEFAULT FALSE
);