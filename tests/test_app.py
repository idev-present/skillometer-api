from datetime import datetime
from sqlalchemy import text


def test_db_connection(db_session):
    """Checks that back-end can query the PostgreSQL from SQLAlchemy with async session."""
    print("Checking connection with async engine 'SQLAlchemy + asyncpg'...")
    result = db_session.execute(statement=text("SELECT current_timestamp;"))
    raw_result = result.scalar()
    assert isinstance(raw_result, datetime)