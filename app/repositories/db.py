import sqlite3
def connect(path):
    db = sqlite3.connect(path, timeout=10)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db
def initialize(path):
    with connect(path) as db:
        db.execute("CREATE TABLE IF NOT EXISTS doctors (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, specialty TEXT NOT NULL, phone TEXT NOT NULL)")
        db.execute("CREATE TABLE IF NOT EXISTS appointments (id INTEGER PRIMARY KEY AUTOINCREMENT, doctor_id INTEGER NOT NULL, patient_name TEXT NOT NULL, appointment_date TEXT NOT NULL, appointment_time TEXT NOT NULL, reason TEXT NOT NULL, FOREIGN KEY(doctor_id) REFERENCES doctors(id) ON DELETE RESTRICT)")
        db.execute("CREATE UNIQUE INDEX IF NOT EXISTS uq_doctor_slot ON appointments(doctor_id, appointment_date, appointment_time)")
