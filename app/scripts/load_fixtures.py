import os
from pathlib import Path

from orjson import orjson
from sqlalchemy import insert, select, func
from sqlalchemy.exc import IntegrityError
from structlog import get_logger

from app.core.config import settings
from app.core.db import db_service
from app.services.dict.db_models import CityDBModel, DivisionDBModel, EmploymentTypeDBModel, QualificationDBModel, \
    SearchStatusDBModel, SkillDBModel

logger = get_logger(__name__)


def read_data(tablename):
    base_path = Path(os.path.dirname(__file__))
    file_path = os.path.join(base_path.absolute().parent, f"fixtures/{tablename}.json")
    logger.info(f"Loading fixtures from {file_path}")
    with open(file_path, "r") as f:
        return orjson.loads(f.read())


def load_dict_cities(session):
    logger.debug("check if filling dict cities")
    count = session.scalar(select(func.count("*")).select_from(CityDBModel))
    logger.debug(f"founded {count} cities in database")
    if count == 0:
        logger.debug("loading dict of cities from fixture")
        fixtures_data = read_data('dict_city')
        logger.info(f"founded {len(fixtures_data)} cities")
        if len(fixtures_data) == 0:
            return None
        try:
            session.execute(
                insert(CityDBModel),
                fixtures_data
            )
        except IntegrityError as e:
            logger.error(e)
        except Exception as e:
            logger.error(e)
        finally:
            logger.debug("loaded dict of cities")


def load_dict_divisions(session):
    logger.debug("check if filling dict divisions")
    count = session.scalar(select(func.count("*")).select_from(DivisionDBModel))
    logger.debug(f"founded {count} divisions in database")
    if count == 0:
        logger.debug("loading dict of divisions from fixture")
        fixtures_data = read_data('dict_division')
        logger.info(f"founded {len(fixtures_data)} divisions")
        if len(fixtures_data) == 0:
            return None
        try:
            session.execute(
                insert(DivisionDBModel),
                fixtures_data,
            )
        except IntegrityError as e:
            logger.error(e)
        except Exception as e:
            logger.error(e)
        finally:
            logger.debug("loaded dict of divisions")


def load_dict_employment_types(session):
    logger.debug("check if filling dict employment types")
    count = session.scalar(select(func.count("*")).select_from(EmploymentTypeDBModel))
    logger.debug(f"founded {count} employment types in database")
    if count == 0:
        logger.debug("loading dict of employment types from fixture")
        fixtures_data = read_data('dict_employment_type')
        logger.info(f"founded {len(fixtures_data)} employment types")
        if len(fixtures_data) == 0:
            return None
        try:
            session.execute(
                insert(EmploymentTypeDBModel),
                fixtures_data,
            )
        except IntegrityError as e:
            logger.error(e)
        except Exception as e:
            logger.error(e)
        finally:
            logger.debug("loaded dict of employment types")


def load_dict_qualifications(session):
    logger.debug("check if filling dict qualifications")
    count = session.scalar(select(func.count("*")).select_from(QualificationDBModel))
    logger.debug(f"founded {count} qualifications in database")
    if count == 0:
        logger.debug("loading dict of qualifications from fixture")
        fixtures_data = read_data('dict_qualification')
        logger.info(f"founded {len(fixtures_data)} qualifications")
        if len(fixtures_data) == 0:
            return None
        try:
            session.execute(
                insert(QualificationDBModel),
                fixtures_data,
            )
        except IntegrityError as e:
            logger.error(e)
        except Exception as e:
            logger.error(e)
        finally:
            logger.debug("loaded dict of qualifications")


def load_dict_search_status(session):
    logger.debug("check if filling dict search status")
    count = session.scalar(select(func.count("*")).select_from(SearchStatusDBModel))
    logger.debug(f"founded {count} search status in database")
    if count == 0:
        logger.debug("loading dict of search status from fixture")
        fixtures_data = read_data('dict_search_status')
        logger.info(f"founded {len(fixtures_data)} search status")
        if len(fixtures_data) == 0:
            return None
        try:
            session.execute(
                insert(SearchStatusDBModel),
                fixtures_data,
            )
        except IntegrityError as e:
            logger.error(e)
        except Exception as e:
            logger.error(e)
        finally:
            logger.debug("loaded dict of search status")


def load_dict_skills(session):
    logger.debug("check if filling dict skills")
    count = session.scalar(select(func.count("*")).select_from(SkillDBModel))
    logger.debug(f"founded {count} skills in database")
    if count == 0:
        logger.debug("loading dict of skills from fixture")
        fixtures_data = read_data('dict_skill')
        logger.info(f"founded {len(fixtures_data)} skills")
        if len(fixtures_data) == 0:
            return None
        try:
            session.execute(
                insert(SkillDBModel),
                fixtures_data,
            )
        except IntegrityError as e:
            logger.error(e)
        except Exception as e:
            logger.error(e)
        finally:
            logger.debug("loaded dict of skill")


def main() -> None:
    logger.debug("Connecting to database")
    db_service.connect(str(settings.DATABASE_DSN))

    with db_service.session_factory() as session:
        load_dict_cities(session)
        load_dict_divisions(session)
        load_dict_employment_types(session)
        load_dict_qualifications(session)
        load_dict_search_status(session)
        load_dict_skills(session)
        # save
        session.commit()
    db_service.disconnect()
    logger.info("Fixtures loaded")


if __name__ == "__main__":
    main()
