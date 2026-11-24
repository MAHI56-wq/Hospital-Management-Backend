from .db import connect, initialize
from ..domain.doctor import Doctor
class DoctorRepository:
    def __init__(self, path):
        self.path = path; initialize(path)
    def add(self, x):
        with connect(self.path) as db:
            cur = db.execute("INSERT INTO doctors(name,specialty,phone) VALUES(?,?,?)",(x.name,x.specialty,x.phone)); x.id=cur.lastrowid
        return x
    def get(self, ident):
        with connect(self.path) as db: r=db.execute("SELECT * FROM doctors WHERE id=?",(ident,)).fetchone()
        return Doctor(r["name"],r["specialty"],r["phone"],r["id"]) if r else None
    def list(self):
        with connect(self.path) as db: rows=db.execute("SELECT * FROM doctors ORDER BY id").fetchall()
        return [Doctor(r["name"],r["specialty"],r["phone"],r["id"]) for r in rows]
    def update(self,x):
        with connect(self.path) as db: db.execute("UPDATE doctors SET name=?,specialty=?,phone=? WHERE id=?",(x.name,x.specialty,x.phone,x.id))
        return x
    def delete(self,ident):
        with connect(self.path) as db:
            cur=db.execute("DELETE FROM doctors WHERE id=?",(ident,)); return cur.rowcount>0
