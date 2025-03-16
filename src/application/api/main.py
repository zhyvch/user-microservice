from contextlib import asynccontextmanager

from fastapi import FastAPI

from application.api.users.handlers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app():
    app = FastAPI(
        title='User Service',
        description='Simple user service',
        docs_url='/api/docs',
        debug=True,
        lifespan=lifespan,
    )
    app.include_router(router, prefix='/users')

    return app
