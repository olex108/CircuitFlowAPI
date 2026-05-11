from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.key import ApiKey

import secrets


async def create_api_key(
        email: EmailStr,
        hashed_password: str,
        hashed_api_key: str,
        is_active: bool,
        session: AsyncSession
) -> ApiKey:
    new_api_key = ApiKey(
        email=email,
        hashed_password=hashed_password,
        hashed_api_key=hashed_api_key,
        is_active=is_active
    )
    session.add(new_api_key)
    try:
        await session.commit()
        await session.refresh(new_api_key)

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )
    except Exception as ex:
        await session.rollback()
        raise ex

    return new_api_key


async def get_api_key_from_db(hashed_api_key: str, session: AsyncSession) -> ApiKey | None:
    query = select(ApiKey).where(ApiKey.hashed_api_key == hashed_api_key)
    result = (await session.execute(query)).scalar_one_or_none()
    return result
