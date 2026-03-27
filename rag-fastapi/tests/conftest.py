from pathlib import Path
import os
import sys
import tempfile
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Run tests against SQLite so they do not depend on a local PostgreSQL server.
TEST_DATABASE_PATH = Path(tempfile.gettempdir()) / f"rag-fastapi-tests-{uuid4().hex}.db"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DATABASE_PATH}"

from app.main import app
from app.db.session import engine


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def unique_username():
    return f"user-{uuid4().hex[:8]}"


def pytest_sessionfinish(session, exitstatus):
    engine.dispose()
    TEST_DATABASE_PATH.unlink(missing_ok=True)
