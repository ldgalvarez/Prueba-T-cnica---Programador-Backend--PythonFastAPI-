from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger

def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logger.exception(f"Unhandled error: {exc}")
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
