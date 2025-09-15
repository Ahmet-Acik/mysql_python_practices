import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import pytest
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, ProgrammingError
from src.db_utils import get_engine

TEST_DB = "test_db"

@pytest.fixture(scope="module")
def test_engine():
    # Create test DB if it doesn't exist
    with get_engine("mysql").connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {TEST_DB}"))
    engine = get_engine(TEST_DB)
    yield engine
    # Teardown: drop test DB after tests
    with get_engine("mysql").connect() as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS {TEST_DB}"))

def test_engine_connection(test_engine):
    with test_engine.connect() as conn:
        result = conn.execute(text("SELECT DATABASE()"))
        db_name = result.scalar()
        assert db_name == TEST_DB

def test_invalid_db():
    from sqlalchemy.exc import ProgrammingError
    with pytest.raises(ProgrammingError):
        bad_engine = get_engine("nonexistent_db_12345")
        with bad_engine.connect() as conn:
            conn.execute(text("SELECT 1"))