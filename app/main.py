import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from structlog import get_logger
from app.api.main import api
from app.core.config import settings
from app.core.db import db_service
from app.core.logger.main import configure_logging
from app.utils.iam_utils import SECRET_KEY

configure_logging()

logger = get_logger(__name__)


def init_app():
    app = FastAPI(
        title="Skillometer API",
        version="0.1.0",
        description="Service for recruiters and applicants",
        contact={
            "name": "IDEV team",
            "email": "info@idev-present.com"
        },
        root_path=settings.API_PREFIX,
    )

    @app.on_event("startup")
    def startup():
        logger.info("startup event")
        db_service.connect(str(settings.DATABASE_DSN))

    @app.on_event("shutdown")
    def shutdown():
        logger.info("shutdown event")
        db_service.disconnect()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(
        SessionMiddleware,
        secret_key=SECRET_KEY,
        session_cookie="access-token",
    )

    app.include_router(api)

    return app

app = init_app()

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_config=None,
        reload=True if settings.ENVIRONMENT == 'LOCAL' else False,
    )
