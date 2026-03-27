from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException

from app.core.config import settings
from app.core.security import verify_token
from app.schemas.rag import QueryRequest, QueryResponse
from app.services.rag_service import RAGService


router = APIRouter()


@lru_cache
def get_rag_service() -> RAGService:
    return RAGService()


@router.get("/test")
def test_rag():
    return {"msg": "RAG working"}


# @router.post("/query", response_model=QueryResponse)
# def query_rag(request: QueryRequest):
#     try:
#         answer = get_rag_service().process_query(request.question)
#         return QueryResponse(answer=answer)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


@router.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest, user: str = Depends(verify_token)):
    try:
        # Depends(verify_token) blocks the route with 401 before this line if auth fails.
        answer = get_rag_service().process_query(request.question)
        return QueryResponse(answer=answer)
    except Exception as e:
        # 500: an unexpected app/runtime error happened while generating the answer.
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/env-test")
def env_test():
    return {"app_name": settings.APP_NAME}
