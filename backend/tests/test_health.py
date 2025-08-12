from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """
    Simple health check endpoint to see if the server responds.
    """
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
