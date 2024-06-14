import logging
from sqlalchemy import select
from structlog import get_logger
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
from app.core.config import settings
from app.core.db import db_service
from app.core.logger.main import configure_logging

MAX_TRIES = 60 * 5  # 5 minutes
WAIT_SECONDS = 1

configure_logging()
logger = get_logger(__name__)


@retry(
    stop=stop_after_attempt(MAX_TRIES),
    wait=wait_fixed(WAIT_SECONDS),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def check_db_connection() -> None:
    try:
        with db_service.session_factory() as session:
            session.execute(statement=select(1))  # Пытаемся создать сессию, чтобы проверить, что БД проснулась
    except Exception as e:
        logger.error(e)
        raise e


def setup_database() -> None:
    logger.info("Setting up database")
    db_service.connect(str(settings.DATABASE_DSN))
    check_db_connection()
    db_service.disconnect()


def main() -> None:
    logger.info("Server setup start")
    setup_database()
    logger.info("Server setup done")


if __name__ == "__main__":
    main()
