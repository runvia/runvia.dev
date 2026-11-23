from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """
    Simple health check endpoint to see if the server responds.
    """
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


def test_no_cors_header_for_other_origins(client: TestClient):
    response = client.get("/api/health", headers={"Origin": "http://localhost:3000"})
    assert "access-control-allow-origin" not in response.headers
