from dataclasses import dataclass
@dataclass
class Doctor:
    name: str
    specialty: str
    phone: str
    id: int | None = None
