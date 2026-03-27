from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


def _build_engine():
    if not settings.DATABASE_URL:
        raise RuntimeError("DATABASE_URL is required and must point to PostgreSQL.")

    engine = create_engine(settings.DATABASE_URL)
    with engine.connect():
        pass
    return engine


engine = _build_engine()
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    pass


def initialize_database() -> None:
    from app.db import models

    models.Base.metadata.create_all(bind=engine)


def commit_or_rollback(db: Session) -> None:
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
