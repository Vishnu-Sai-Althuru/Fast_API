from fastapi import FastAPI

from .api.routes import admin, auth, rag

from app.core.config import settings
from app.db.session import initialize_database

app = FastAPI(title=settings.APP_NAME)

initialize_database()

app.include_router(rag.router, prefix="/rag", tags=["RAG"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])


@app.get("/")
def root():
    return {"message": "Vishnu_Server running"}
