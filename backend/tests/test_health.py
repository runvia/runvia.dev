from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """
    Simple health check endpoint to see if the server responds.
    """
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
