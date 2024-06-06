from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Database:
    def __init__(self):
        self.__session = None
        self.__engine = None

    def connect(self, dsn):
        self.__engine = create_async_engine(dsn)
        self.__session = async_sessionmaker(
            bind=self.__engine,
            autocommit=False,
        )

    async def disconnect(self):
        self.__engine.dispose()

    async def get_db(self):
        async with self.__session() as session:
            yield session


db = Database()
