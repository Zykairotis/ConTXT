"""
Tests for the API endpoints.
"""
from fastapi.testclient import TestClient

from Backend.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "AI Context Builder API is running"}


def test_process_url_endpoint():
    """Test the process-url endpoint."""
    response = client.post(
        "/api/v1/process-url",
        json={"url": "https://example.com", "depth": 1},
    )
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "processing"


def test_process_status_endpoint():
    """Test the process status endpoint."""
    # First create a job
    response = client.post(
        "/api/v1/process-url",
        json={"url": "https://example.com", "depth": 1},
    )
    job_id = response.json()["job_id"]
    
    # Then check its status
    response = client.get(f"/api/v1/process/{job_id}")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "progress" in data 