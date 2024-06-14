from typing import Optional

from sqlalchemy import create_engine, Engine
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from structlog import get_logger

from app.core.config import settings
from app.core.exceptions import ServerError, ConflictError, NotFoundError


class Base:
    __allow_unmapped__ = True


BaseDBModel = declarative_base(cls=Base)

logger = get_logger(__name__)


class Database:
    def __init__(self):
        self.dsn = None
        self.session_factory: Optional[sessionmaker] = None
        self.__engine: Optional[Engine] = None

    def connect(self, dsn):
        self.dsn = dsn
        self.__engine = create_engine(dsn)
        self.session_factory = sessionmaker(
            bind=self.__engine,
            autocommit=False,
            autoflush=False,
            class_=Session
        )

    def disconnect(self):
        self.__engine.dispose()

    def get_db(self):
        """Creates FastAPI dependency for generation of SQLAlchemy Session.

        Yields:
            Session: SQLAlchemy Session.
        """
        with self.session_factory() as session:
            try:
                yield session
                session.commit()
            except IntegrityError as error:
                session.rollback()
                if "duplicate" in error.args[0]:
                    raise ConflictError(
                        message=str(error.orig.args[0].split("\n")[-1]) if settings.LOG_LEVEL == "DEBUG" else "Conflict",
                    )
                raise ServerError(
                    message=str(error) if settings.LOG_LEVEL == "DEBUG" else "Internal server error."
                )
            except NoResultFound as error:
                session.rollback()
                raise NotFoundError(message=str(error) if settings.LOG_LEVEL == "DEBUG" else "Not found")
            finally:
                session.close()