from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.key import CreateApi, ApiKeyOut
from src.config.database import get_session
from src.crud.key import create_api_key

from typing import Annotated

from src.services.api_keys import ApiKeyHandler
from src.services.password import PasswordHandler

router = APIRouter()


@router.post("/create_api_key", response_model=ApiKeyOut)
async def register(
        register_data: CreateApi,
        session: Annotated[AsyncSession, Depends(get_session)]
):
    """Эндпроинт для создания ключа по почте пользователя"""

    hashed_password = PasswordHandler.get_hashed_password(register_data.password)
    user_api_key = ApiKeyHandler()

    try:
        await create_api_key(
            email=register_data.email,
            hashed_password=hashed_password,
            hashed_api_key=user_api_key.hashed_api_key,
            is_active=True, # По умолчанию ключ активный, поменять на задание по верификации
            session=session
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Registration server error"
        )

    return {"api_key": user_api_key.api_key}
