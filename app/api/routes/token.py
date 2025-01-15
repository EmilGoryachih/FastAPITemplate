from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.models.dtoModels.TockenDTO import TokenDTO
from app.models.dtoModels.UserDTO import UserDTO
from app.infrastructure.db.session import fastapi_get_db
from app.services.authorization import AuthService, get_current_user_service

router = APIRouter()


@router.post("/get-token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: AsyncSession = Depends(fastapi_get_db),
        auth_service: AuthService = Depends(),
):
    """
    Эндпоинт для получения токена доступа.
    """
    return await auth_service.login_for_access_token(form_data, session)


@router.get("/current_user", response_model=UserDTO)
async def read_users_me(
    current_user: Annotated[UserDTO, Depends(get_current_user_service)]
):
    return current_user
