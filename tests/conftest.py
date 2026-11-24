import pytest
from app import create_app
@pytest.fixture
def app(tmp_path):
    app=create_app({"TESTING":True,"DATABASE_PATH":str(tmp_path/"test.db"),"LOG_LEVEL":"CRITICAL"})
    yield app
@pytest.fixture
def client(app): return app.test_client()
@pytest.fixture
def doctor(client):
    r=client.post("/api/doctors",json={"name":"Dr. Ayesha Rahman","specialty":"Cardiology","phone":"01700000000"})
    assert r.status_code==201
    return r.get_json()
