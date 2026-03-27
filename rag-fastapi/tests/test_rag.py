# from fastapi.testclient import TestClient
# import requests
# from uuid import uuid4

# import app.services.llm_service as llm_service
# import app.api.routes.rag as rag_routes
# from app.api.routes.rag import get_rag_service
# from app.services.vector_db import VectorDB
# from app.main import app

# client = TestClient(app)


# def get_auth_headers():
#     username = f"admin-{uuid4().hex[:8]}"
#     password = "admin123"

#     signup_response = client.post(
#         "/auth/signup",
#         json={"username": username, "password": password},
#     )
#     assert signup_response.status_code == 200, signup_response.text

#     response = client.post(
#         "/auth/login",
#         data={"username": username, "password": password},
#     )
#     assert response.status_code == 200, response.text
#     token = response.json()["access_token"]
#     return {"Authorization": f"Bearer {token}"}


# def test_rag():
#     response = client.get("/rag/test")
#     assert response.status_code == 200
#     assert response.json()["msg"] == "RAG working"


# def test_signup_rejects_short_credentials():
#     response = client.post(
#         "/auth/signup",
#         json={"username": "ab", "password": "123"},
#     )

#     assert response.status_code == 422


# def test_signup_rejects_blank_username():
#     response = client.post(
#         "/auth/signup",
#         json={"username": "   ", "password": "secret123"},
#     )

#     assert response.status_code == 422
#     assert response.json()["detail"] == "Invalid request payload"
#     assert any(error["loc"][-1] == "username" for error in response.json()["errors"])


# def test_duplicate_signup_returns_400():
#     username = f"duplicate-{uuid4().hex[:8]}"
#     payload = {"username": username, "password": "secret123"}

#     first_response = client.post("/auth/signup", json=payload)
#     second_response = client.post("/auth/signup", json=payload)

#     assert first_response.status_code == 200, first_response.text
#     assert second_response.status_code == 400, second_response.text


# def test_rag_query_falls_back_when_ollama_is_unavailable(monkeypatch):
#     def fake_post(*args, **kwargs):
#         raise requests.RequestException("ollama down")

#     get_rag_service.cache_clear()
#     monkeypatch.setattr(llm_service.requests, "post", fake_post)

#     response = client.post(
#         "/rag/query",
#         json={"question": "What is AI?"},
#         headers=get_auth_headers(),
#     )

#     assert response.status_code == 200
#     assert "Ollama is unavailable right now." in response.json()["answer"]


# def test_rag_query_rejects_blank_question():
#     response = client.post(
#         "/rag/query",
#         json={"question": "   "},
#         headers=get_auth_headers(),
#     )

#     assert response.status_code == 422
#     assert response.json()["detail"] == "Invalid request payload"
#     assert any(error["loc"][-1] == "question" for error in response.json()["errors"])


# def test_rag_query_returns_503_when_service_initialization_fails(monkeypatch):
#     def broken_rag_service():
#         raise RuntimeError("documents missing")

#     get_rag_service.cache_clear()
#     monkeypatch.setattr(rag_routes, "RAGService", broken_rag_service)

#     response = client.post(
#         "/rag/query",
#         json={"question": "What is AI?"},
#         headers=get_auth_headers(),
#     )

#     assert response.status_code == 503
#     assert response.json() == {"detail": "RAG service is unavailable right now."}


# def test_rag_query_returns_safe_500_for_processing_errors(monkeypatch):
#     def broken_search(self, query, k=2):
#         raise RuntimeError("vector database failed")

#     get_rag_service.cache_clear()
#     monkeypatch.setattr(VectorDB, "search", broken_search)

#     response = client.post(
#         "/rag/query",
#         json={"question": "What is AI?"},
#         headers=get_auth_headers(),
#     )

#     assert response.status_code == 500
#     assert response.json() == {"detail": "Unable to process the question right now."}

def test_rag_query_with_mock(client, unique_username, monkeypatch):

    # 🔥 Mock LLM response
    def mock_generate(self, question, context):
        return "mocked answer"

    monkeypatch.setattr(
        "app.services.llm_service.LLMService.generate",
        mock_generate
    )

    # Create user + login
    client.post("/auth/signup", json={
        "username": unique_username,
        "password": "secret123",
    })

    login = client.post("/auth/login", data={
        "username": unique_username,
        "password": "secret123"
    })

    assert login.status_code == 200, login.text
    token = login.json()["access_token"]

    # Call protected API
    response = client.post(
        "/rag/query",
        json={"question": "What is AI?"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "mocked answer"
