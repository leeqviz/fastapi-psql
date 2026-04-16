import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .configs import settings
from .db import psql_conn
from .routers import api_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    # await psql_conn.init()
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

logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error caught: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal Server Error",
            "details": str(exc) if app.debug else None
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        settings.app.entrypoint, 
        host=settings.app.host, 
        port=settings.app.port, 
        reload=settings.app.reload
    )