def payload(doctor_id,**changes):
    d={"doctor_id":doctor_id,"patient_name":"Mahi","appointment_date":"2026-12-02","appointment_time":"11:00","reason":"Regular checkup"}
    d.update(changes); return d
def test_appointment_full_crud(client,doctor):
    r=client.post("/api/appointments",json=payload(doctor["id"]))
    assert r.status_code==201
    i=r.get_json()["id"]; assert r.headers["Location"].endswith(f"/api/appointments/{i}")
    assert client.get("/api/appointments").status_code==200
    assert client.get(f"/api/appointments/{i}").status_code==200
    r=client.put(f"/api/appointments/{i}",json={"patient_name":"Updated Patient","appointment_time":"12:00"})
    assert r.status_code==200 and r.get_json()["patient_name"]=="Updated Patient"
    assert client.delete(f"/api/appointments/{i}").status_code==204
    assert client.get(f"/api/appointments/{i}").status_code==404
def test_duplicate_slot_conflict(client,doctor):
    assert client.post("/api/appointments",json=payload(doctor["id"])).status_code==201
    r=client.post("/api/appointments",json=payload(doctor["id"]))
    assert r.status_code==409 and r.get_json()["code"]=="conflict"
def test_invalid_date_time_422(client,doctor):
    r=client.post("/api/appointments",json=payload(doctor["id"],appointment_date="bad",appointment_time="25:99"))
    assert r.status_code==422 and "appointment_date" in r.get_json()["errors"]
def test_unknown_doctor_422(client):
    assert client.post("/api/appointments",json=payload(9999)).status_code==422
def test_unknown_appointment_404(client):
    assert client.get("/api/appointments/9999").status_code==404
