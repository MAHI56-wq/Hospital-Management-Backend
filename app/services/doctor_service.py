import logging, sqlite3
from ..domain.doctor import Doctor
from ..errors import NotFound, ValidationFailed, Conflict
log=logging.getLogger(__name__)
class DoctorService:
    def __init__(self,repo): self.repo=repo
    @staticmethod
    def validate(data,creating):
        if not isinstance(data,dict): return {"body":"A JSON object is required"}
        errors={}
        for f in (["name","specialty","phone"] if creating else []):
            if not isinstance(data.get(f),str) or not data[f].strip(): errors[f]="This field is required"
        for f in ("name","specialty","phone"):
            if f in data and (not isinstance(data[f],str) or not data[f].strip()): errors[f]="Must be a non-empty string"
        return errors
    def create(self,data):
        e=self.validate(data,True)
        if e: raise ValidationFailed(e)
        x=self.repo.add(Doctor(*(data[f].strip() for f in ("name","specialty","phone"))))
        log.info("doctor created id=%s",x.id); return x
    def get(self,i):
        x=self.repo.get(i)
        if not x: raise NotFound(f"Doctor {i} was not found")
        return x
    def list(self): return self.repo.list()
    def update(self,i,data):
        x=self.get(i); e=self.validate(data,False)
        if e: raise ValidationFailed(e)
        for f in ("name","specialty","phone"):
            if f in data: setattr(x,f,data[f].strip())
        self.repo.update(x); log.info("doctor updated id=%s",i); return x
    def delete(self,i):
        self.get(i)
        try: self.repo.delete(i)
        except sqlite3.IntegrityError as exc: raise Conflict("Doctor has appointments and cannot be deleted") from exc
        log.info("doctor deleted id=%s",i)
