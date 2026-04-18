from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from sqlalchemy.exc import DatabaseError

from src.core import AppException, configure_logging
from src.handlers import (
    app_error_handler,
    database_error_handler,
    error_handler,
    validation_error_handler,
)
from src.middlewares import LogRequestMiddleware, ResponseTimeMiddleware

from .configs import settings
from .db import psql_conn
from .routers import api_router

configure_logging()


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield
    await psql_conn.engine.dispose()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.origins,
    allow_methods=settings.cors.methods,
    allow_headers=settings.cors.headers,
    allow_credentials=settings.cors.credentials,  # Allows cookies
)

app.add_middleware(LogRequestMiddleware)

app.add_middleware(ResponseTimeMiddleware)  # will be the first


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(api_router, prefix=settings.api.prefix)

app.add_exception_handler(Exception, error_handler)
app.add_exception_handler(AppException, app_error_handler)  # type: ignore
app.add_exception_handler(DatabaseError, database_error_handler)  # type: ignore
app.add_exception_handler(ValidationError, validation_error_handler)  # type: ignore


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        settings.app.entrypoint,
        host=settings.app.host,
        port=settings.app.port,
        reload=settings.app.reload,
    )
