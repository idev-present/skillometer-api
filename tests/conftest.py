import pytest
from app.core.config import settings
from sqlalchemy_utils import database_exists, create_database, drop_database

from app.core.db import db_service

TEST_DB_NAME = 'test_db'


@pytest.fixture(scope='function')
@pytest.mark.asyncio
async def db_session():
    db_dsn = settings.DATABASE_DSN
    test_db_dsn = str(db_dsn).replace(f"{db_dsn.path}", f"/{TEST_DB_NAME}")
    print(str(test_db_dsn))
    if await database_exists(test_db_dsn):
        await drop_database(test_db_dsn)

    await create_database(test_db_dsn)
    await db_service.connect(test_db_dsn)

    yield db_service.get_db

    await db_service.disconnect()
