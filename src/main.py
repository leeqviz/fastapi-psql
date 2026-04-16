from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .configs import settings
from .db import psql_conn
from .routers import api_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await psql_conn.init()
    yield
    await psql_conn.dispose()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.origins,
    allow_methods=settings.cors.methods,
    allow_headers=settings.cors.headers,
    allow_credentials=settings.cors.credentials,   # Allows cookies
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(api_router, prefix=settings.api.prefix)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        settings.app.entrypoint, 
        host=settings.app.host, 
        port=settings.app.port, 
        reload=settings.app.reload
    )