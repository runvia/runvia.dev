from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_cv():
    resp = client.get("/api/cv")
    assert resp.status_code == 200
    data = resp.json()

    assert "name" in data and data['name'] == "Niclas Andersen"
    assert isinstance(data['experience'], list)
    assert isinstance(data['skills'], list)