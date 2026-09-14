from __future__ import annotations

from typing import TYPE_CHECKING

from src.main import InvestigationStatus

if TYPE_CHECKING:
    from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    assert body["service"] == "ai-sre-copilot"


def test_investigate_returns_queued(client: TestClient) -> None:
    payload = {
        "title": "Pod crashing in production",
        "service": "api-gateway",
        "severity": "critical",
        "description": "Pod restarted 50 times in the last hour",
    }
    response = client.post("/api/v1/incidents/investigate", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["incident"] == "Pod crashing in production"
    assert body["status"] == InvestigationStatus.queued
    assert isinstance(body["next_steps"], list)
    assert len(body["next_steps"]) > 0


def test_investigate_defaults(client: TestClient) -> None:
    payload = {"title": "Test incident", "service": "auth-service"}
    response = client.post("/api/v1/incidents/investigate", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == InvestigationStatus.queued


def test_investigate_invalid_severity(client: TestClient) -> None:
    payload = {
        "title": "Test",
        "service": "test",
        "severity": "nonexistent",
    }
    response = client.post("/api/v1/incidents/investigate", json=payload)
    assert response.status_code == 422


def test_investigate_missing_required_fields(client: TestClient) -> None:
    response = client.post("/api/v1/incidents/investigate", json={})
    assert response.status_code == 422
