def test_doctor_full_crud(client):
    r=client.post("/api/doctors",json={"name":"Dr Karim","specialty":"Medicine","phone":"01811111111"})
    assert r.status_code==201
    i=r.get_json()["id"]; assert r.headers["Location"].endswith(f"/api/doctors/{i}")
    assert client.get("/api/doctors").status_code==200
    assert client.get(f"/api/doctors/{i}").get_json()["name"]=="Dr Karim"
    r=client.put(f"/api/doctors/{i}",json={"specialty":"Neurology"})
    assert r.status_code==200 and r.get_json()["specialty"]=="Neurology"
    assert client.delete(f"/api/doctors/{i}").status_code==204
    assert client.get(f"/api/doctors/{i}").status_code==404
def test_doctor_validation_422(client):
    r=client.post("/api/doctors",json={"name":"","specialty":"Surgery"})
    assert r.status_code==422 and "phone" in r.get_json()["errors"]
    assert r.content_type.startswith("application/problem+json")
def test_doctor_delete_conflict(client,doctor):
    client.post("/api/appointments",json={"doctor_id":doctor["id"],"patient_name":"Rafi","appointment_date":"2026-12-01","appointment_time":"10:30","reason":"Checkup"})
    assert client.delete(f'/api/doctors/{doctor["id"]}').status_code==409
