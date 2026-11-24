from dataclasses import dataclass
@dataclass
class Appointment:
    doctor_id: int
    patient_name: str
    appointment_date: str
    appointment_time: str
    reason: str
    id: int | None = None
