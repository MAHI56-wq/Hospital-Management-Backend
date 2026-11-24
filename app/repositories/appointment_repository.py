import sqlite3
from .db import connect, initialize
from ..domain.appointment import Appointment
class AppointmentRepository:
    def __init__(self,path):
        self.path=path; initialize(path)
    def add(self,x):
        try:
            with connect(self.path) as db:
                cur=db.execute("INSERT INTO appointments(doctor_id,patient_name,appointment_date,appointment_time,reason) VALUES(?,?,?,?,?)",
                    (x.doctor_id,x.patient_name,x.appointment_date,x.appointment_time,x.reason)); x.id=cur.lastrowid
        except sqlite3.IntegrityError as exc:
            raise ValueError("The doctor already has an appointment at this date and time") from exc
        return x
    def get(self,ident):
        with connect(self.path) as db: r=db.execute("SELECT * FROM appointments WHERE id=?",(ident,)).fetchone()
        return self._make(r) if r else None
    def list(self):
        with connect(self.path) as db: rows=db.execute("SELECT * FROM appointments ORDER BY appointment_date,appointment_time").fetchall()
        return [self._make(r) for r in rows]
    def update(self,x):
        try:
            with connect(self.path) as db:
                db.execute("UPDATE appointments SET doctor_id=?,patient_name=?,appointment_date=?,appointment_time=?,reason=? WHERE id=?",
                    (x.doctor_id,x.patient_name,x.appointment_date,x.appointment_time,x.reason,x.id))
        except sqlite3.IntegrityError as exc:
            raise ValueError("The doctor already has an appointment at this date and time") from exc
        return x
    def delete(self,ident):
        with connect(self.path) as db:
            cur=db.execute("DELETE FROM appointments WHERE id=?",(ident,)); return cur.rowcount>0
    @staticmethod
    def _make(r):
        return Appointment(r["doctor_id"],r["patient_name"],r["appointment_date"],r["appointment_time"],r["reason"],r["id"])
