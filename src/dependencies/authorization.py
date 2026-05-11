from typing import Annotated

from fastapi import Security, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.config.database import get_session

from src.models.key import ApiKey
from src.crud.key import get_api_key_from_db
from src.services.api_keys import ApiKeyHandler

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_api_key(
        user_api_key: Annotated[str, Security(api_key_header)],
        session: Annotated[AsyncSession, Depends(get_session)]
):  # Убрал возвращаемый тип ApiKey (Pydantic), так как вернется модель БД
    if not user_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="API Key missing"
        )

    key_handler = ApiKeyHandler(user_api_key)

    # ВЫЗОВ ПЕРЕИМЕНОВАННОЙ ФУНКЦИИ (исправлена рекурсия)
    api_key_db = await get_api_key_from_db(key_handler.hashed_api_key, session)

    if api_key_db is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API Key"
        )
    if not api_key_db.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Your API Key is inactive"
        )
    return api_key_db