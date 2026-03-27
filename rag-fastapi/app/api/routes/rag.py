from functools import lru_cache

from fastapi import APIRouter, Depends

from app.core.config import settings
from app.core.exceptions import AppError, ServiceUnavailableError
from app.core.security import verify_token
from app.schemas.rag import QueryRequest, QueryResponse
from app.services.rag_service import RAGService


router = APIRouter()


@lru_cache
def get_rag_service() -> RAGService:
    try:
        return RAGService()
    except AppError:
        raise
    except Exception as exc:
        raise ServiceUnavailableError("RAG service is unavailable right now.") from exc


@router.get("/test")
def test_rag():
    return {"msg": "RAG working"}


@router.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest, user: dict = Depends(verify_token)):
    # Depends(verify_token) blocks the route with 401 before this line if auth fails.
    answer = get_rag_service().process_query(request.question)
    return QueryResponse(answer=answer)


@router.get("/env-test")
def env_test():
    return {"app_name": settings.APP_NAME}
