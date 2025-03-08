from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger

async def global_exception_handler(request: Request, exc: Exception):
    # Проверяем тип ошибки
    if isinstance(exc, HTTPException):
        logger.error(f"HTTPException occurred: {exc.detail} - Status code: {exc.status_code} "
                     f"while processing request {request.method} {request.url}")
        # Возвращаем только message из detail, исключая код ошибки
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": f"HTTP {exc.status_code} Error", "message": exc.detail}
        )
    else:
        logger.error(f"Unexpected exception occurred: {type(exc).__name__} - {str(exc)} "
                     f"while processing request {request.method} {request.url}")
        # Возвращаем стандартный ответ с кодом 500
        return JSONResponse(
            status_code=500,
            content={"error": "Internal Server Error", "message": str(exc)}
        )
