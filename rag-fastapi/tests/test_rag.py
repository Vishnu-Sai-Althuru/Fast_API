from fastapi.testclient import TestClient
import requests
from uuid import uuid4

import app.services.llm_service as llm_service
from app.api.routes.rag import get_rag_service
from app.main import app

client = TestClient(app)


def get_auth_headers():
    username = f"admin-{uuid4().hex[:8]}"
    password = "admin123"

    signup_response = client.post(
        "/auth/signup",
        json={"username": username, "password": password},
    )
    assert signup_response.status_code == 200, signup_response.text

    response = client.post(
        "/auth/login",
        data={"username": username, "password": password},
    )
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_rag():
    response = client.get("/rag/test")
    assert response.status_code == 200
    assert response.json()["msg"] == "RAG working"


def test_signup_rejects_short_credentials():
    response = client.post(
        "/auth/signup",
        json={"username": "ab", "password": "123"},
    )

    assert response.status_code == 422


def test_duplicate_signup_returns_400():
    username = f"duplicate-{uuid4().hex[:8]}"
    payload = {"username": username, "password": "secret123"}

    first_response = client.post("/auth/signup", json=payload)
    second_response = client.post("/auth/signup", json=payload)

    assert first_response.status_code == 200, first_response.text
    assert second_response.status_code == 400, second_response.text


def test_rag_query_falls_back_when_ollama_is_unavailable(monkeypatch):
    def fake_post(*args, **kwargs):
        raise requests.RequestException("ollama down")

    get_rag_service.cache_clear()
    monkeypatch.setattr(llm_service.requests, "post", fake_post)

    response = client.post(
        "/rag/query",
        json={"question": "What is AI?"},
        headers=get_auth_headers(),
    )

    assert response.status_code == 200
    assert "Ollama is unavailable right now." in response.json()["answer"]
