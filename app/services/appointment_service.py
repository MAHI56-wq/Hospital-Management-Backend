import logging
from datetime import date,time
from ..domain.appointment import Appointment
from ..errors import NotFound,ValidationFailed,Conflict
log=logging.getLogger(__name__)
def valid_date(v):
    try: date.fromisoformat(v); return True
    except (ValueError,TypeError): return False
def valid_time(v):
    try: time.fromisoformat(v); return isinstance(v,str) and len(v)==5
    except (ValueError,TypeError): return False
class AppointmentService:
    def __init__(self,repo,doctor_repo): self.repo,self.doctor_repo=repo,doctor_repo
    @staticmethod
    def validate(data,creating):
        if not isinstance(data,dict): return {"body":"A JSON object is required"}
        rules={"doctor_id":lambda x:isinstance(x,int) and x>0,
               "patient_name":lambda x:isinstance(x,str) and bool(x.strip()),
               "appointment_date":valid_date,"appointment_time":valid_time,
               "reason":lambda x:isinstance(x,str) and bool(x.strip())}
        errors={}
        for f,check in rules.items():
            if creating and f not in data: errors[f]="This field is required"
            elif f in data and not check(data[f]): errors[f]="Invalid value"
        return errors
    def ensure_doctor(self,i):
        if not self.doctor_repo.get(i): raise ValidationFailed({"doctor_id":"Doctor does not exist"})
    def create(self,data):
        e=self.validate(data,True)
        if e: raise ValidationFailed(e)
        self.ensure_doctor(data["doctor_id"])
        x=Appointment(data["doctor_id"],data["patient_name"].strip(),data["appointment_date"],data["appointment_time"],data["reason"].strip())
        try: x=self.repo.add(x)
        except ValueError as exc: raise Conflict(str(exc)) from exc
        log.info("appointment created id=%s",x.id); return x
    def get(self,i):
        x=self.repo.get(i)
        if not x: raise NotFound(f"Appointment {i} was not found")
        return x
    def list(self): return self.repo.list()
    def update(self,i,data):
        x=self.get(i); e=self.validate(data,False)
        if e: raise ValidationFailed(e)
        doctor_id=data.get("doctor_id",x.doctor_id); self.ensure_doctor(doctor_id)
        for f in ("patient_name","appointment_date","appointment_time","reason"):
            if f in data: setattr(x,f,data[f].strip() if f in ("patient_name","reason") else data[f])
        x.doctor_id=doctor_id
        try: self.repo.update(x)
        except ValueError as exc: raise Conflict(str(exc)) from exc
        log.info("appointment updated id=%s",i); return x
    def delete(self,i):
        self.get(i); self.repo.delete(i); log.info("appointment deleted id=%s",i)
