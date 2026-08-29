import os

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    if not os.getenv("DATABASE_URL"):
        pytest.skip("DATABASE_URL is not configured for API integration tests")

    from app.main import app

    return TestClient(app)


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "X-Fin"
    assert body["status"] == "healthy"


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_intelligence_health(client):
    response = client.get("/intelligence/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
