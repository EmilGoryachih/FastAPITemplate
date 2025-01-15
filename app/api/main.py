from fastapi import APIRouter

from app.api.routes import UserRout
from app.api.routes import token

api_router = APIRouter()

api_router.include_router(UserRout.router, prefix="/user", tags=["user"])
api_router.include_router(token.router, prefix="/token", tags=["tocken"])

