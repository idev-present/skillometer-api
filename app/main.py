import uvicorn
from fastapi import FastAPI

from app.api.main import api
from app.core.db import db
from app.core.settings import settings


def init_app():
    app = FastAPI(
        title=settings.PROJECT_NAME,
    )

    @app.on_event("startup")
    def startup():
        print("startup event")
        db.connect(str(settings.DATABASE_DSN))

    @app.on_event("shutdown")
    def shutdown():
        print("shutdown event")
        db.disconnect()

    app.include_router(api)

    return app


app = init_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
