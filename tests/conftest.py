import asyncio
import typing

import pytest
import pytest_asyncio
from _pytest.monkeypatch import MonkeyPatch
from sqlalchemy import Engine, create_engine, event
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
    async_scoped_session,
    AsyncConnection,
)
from sqlalchemy.orm import close_all_sessions, sessionmaker, Session
from pytest_alembic import Config, runner

from app.core.config import settings
from sqlalchemy_utils import database_exists, create_database, drop_database

from app.core.db import db_service


@pytest.fixture(scope="session")
def monkeypatch_session() -> MonkeyPatch:
    """Create monkeypatch for session scope.

    Yields:
        monkeypatch (MonkeyPatch): MonkeyPatch instance with `session` (one time per tests run) scope.
    """
    monkeypatch = MonkeyPatch()
    try:
        yield monkeypatch
    finally:
        monkeypatch.undo()


@pytest.fixture(scope='session', autouse=True)
def _mock_db_dsn(monkeypatch_session: MonkeyPatch):
    TEST_DB_NAME = 'test_db'
    monkeypatch_session.setattr(target=settings, name="DATABASE_DBNAME", value=TEST_DB_NAME)


@pytest.fixture(scope='session', autouse=True)
def _create_db(_mock_db_dsn: None, monkeypatch_session: MonkeyPatch):
    """Recreates `test` database for tests."""
    print("\n----- CREATE DB\n")
    if database_exists(str(settings.DATABASE_DSN)):
        drop_database(str(settings.DATABASE_DSN))
    create_database(str(settings.DATABASE_DSN))
    yield
    print("\n----- DELETE DB\n")
    close_all_sessions()
    drop_database(str(settings.DATABASE_DSN))


@pytest.fixture(scope="session")
def db_engine() -> Engine:
    """Create sync database engine and dispose it after all tests.

    Yields:
        engine (Engine): SQLAlchemy Engine instance.
    """
    engine = create_engine(url=str(settings.DATABASE_DSN), echo=False)
    try:
        yield engine
    finally:
        close_all_sessions()
        engine.dispose()


@pytest.fixture(scope="session")
def alembic_config() -> Config:
    """Initialize pytest_alembic Config."""
    return Config()


@pytest.fixture(scope="session")
def alembic_engine(db_engine: Engine) -> Engine:
    """Proxy sync_db_engine to pytest_alembic (make it as a default engine)."""
    return db_engine


@pytest.fixture(scope="session")
def alembic_runner(alembic_config: Config, alembic_engine: Engine) -> typing.Generator[runner, None, None]:
    """Setup runner for pytest_alembic (combine Config and engine)."""
    config = Config.from_raw_config(alembic_config)
    with runner(config=config, engine=alembic_engine) as alembic_runner:
        yield alembic_runner


@pytest.fixture(scope="session", autouse=True)
def _apply_migrations(
        _create_db: None,
        alembic_runner: runner,
        alembic_engine: Engine,
) -> typing.Generator[None, None, None]:
    """Applies all migrations from base to head (via pytest_alembic)."""
    alembic_runner.migrate_up_to(revision="head")
    yield
    # Disabled, because delete database after test_run
    # alembic_runner.migrate_down_to(revision="base")


@pytest.fixture(scope="session")
def session_factory(db_engine: Engine) -> sessionmaker:
    """Create async session factory."""
    return sessionmaker(bind=db_engine, expire_on_commit=False, class_=Session)


@pytest.fixture(scope="function")
def db_session(session_factory):
    with session_factory() as session:
        try:
            yield session
        except Exception as error:
            session.rollback()
            raise error
        finally:
            session.rollback()
            session.close()
