from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import fastapi_get_db
from app.models.dtoModels.RegistrationDTO import RegistrationDTO
from app.services.UserCrud import add_user

router = APIRouter()

@router.post("/register", status_code=201)
async def register(user: RegistrationDTO, session: AsyncSession = Depends(fastapi_get_db)):
    user = await add_user(username=user.name, email=user.email, password=user.password, session=session)
    return user