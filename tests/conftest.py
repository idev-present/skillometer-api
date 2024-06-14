import asyncio
import typing

import pytest
import pytest_asyncio
from _pytest.monkeypatch import MonkeyPatch
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import close_all_sessions, sessionmaker, Session, scoped_session
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


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session', autouse=True)
def _mock_db_dsn(monkeypatch_session: MonkeyPatch):
    TEST_DB_NAME = 'test_db'
    monkeypatch_session.setattr(target=settings, name="DATABASE_DBNAME", value=TEST_DB_NAME)
    monkeypatch_session.setattr(target=settings, name="DATABASE_DRIVER", value="postgresql")


@pytest.fixture(scope='session', autouse=True)
def _create_db(_mock_db_dsn: None, monkeypatch_session: MonkeyPatch):
    """Recreates `test` database for tests."""
    print("\n----- CREATE DB\n")
    if database_exists(str(settings.DATABASE_DSN)):
        drop_database(str(settings.DATABASE_DSN))
    create_database(str(settings.DATABASE_DSN))
    monkeypatch_session.setattr(target=settings, name="DATABASE_DRIVER", value="postgresql+asyncpg")
    yield
    print("\n----- DELETE DB\n")
    monkeypatch_session.setattr(target=settings, name="DATABASE_DRIVER", value="postgresql")
    close_all_sessions()
    drop_database(str(settings.DATABASE_DSN))


@pytest.fixture(scope="session")
async def async_db_engine(event_loop: asyncio.AbstractEventLoop) -> AsyncEngine:
    """Create async database engine and dispose it after all tests.

    Yields:
        async_engine (AsyncEngine): SQLAlchemy AsyncEngine instance.
    """
    async_engine = create_async_engine(url=str(settings.DATABASE_DSN), echo=False, feature=True)
    try:
        yield async_engine
    finally:
        close_all_sessions()
        await async_engine.dispose()


@pytest.fixture(scope="session")
def alembic_config() -> Config:
    """Initialize pytest_alembic Config."""
    return Config()


@pytest.fixture(scope="session")
def alembic_engine(async_db_engine: Engine) -> Engine:
    """Proxy async_db_engine to pytest_alembic (make it as a default engine)."""
    return async_db_engine


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
    # alembic_runner.migrate_down_to(revision="base")


@pytest_asyncio.fixture()
async def db_engine(event_loop):
    engine = create_async_engine(
        str(settings.DATABASE_DSN),
        echo=False,
        future=True,
    )

    yield engine

    engine.sync_engine.dispose()


@pytest_asyncio.fixture()
async def db_session(db_engine):
    SessionLocal = async_sessionmaker(
        bind=db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    async with db_engine.connect() as conn:
        tsx = await conn.begin()
        async with SessionLocal(bind=conn) as session:
            nested_tsx = await conn.begin_nested()
            yield session

            if nested_tsx.is_active:
                await nested_tsx.rollback()
            await tsx.rollback()
