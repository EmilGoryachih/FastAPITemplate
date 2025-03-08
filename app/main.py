from fastapi import FastAPI, APIRouter, Request, HTTPException
import sys
import logging
from loguru import logger
import uvicorn
from environs import Env

from app.infrastructure.exception_handler import global_exception_handler
from app.infrastructure.init_db import init_db
from app.api.main import api_router

env = Env()
env.read_env()
logging.basicConfig(level=logging.INFO)

# Настройка loguru для логирования в файл и на консоль
logger.remove()  # Удаляем стандартную настройку loguru
logger.add("app.log", rotation="10 MB", level="INFO")  # Логи в файл
logger.add(sys.stdout, level="INFO")  # Логи на консоль

# Настройка роутеров
main_router = APIRouter()
main_router.include_router(api_router)

app = FastAPI()
app.include_router(main_router, prefix="/api")
app.add_exception_handler(Exception, global_exception_handler)


# Мидлвар для логирования HTTP-запросов
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP Exception: {exc.detail} - {exc.status_code}")
    return await global_exception_handler(request, exc)


# Событие старта приложения
@app.on_event("startup")
async def on_startup():
    await init_db()


# Запуск приложения
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
