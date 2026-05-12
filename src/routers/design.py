from fastapi import APIRouter, HTTPException, Depends, status
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_session
from src.crud.design import (
    create_new_design,
    update_design_by_id,
    get_design_by_id,
    create_design_params_by_design_id,
    update_design_params_by_design_id,
    get_design_info_by_design_id,
)
from src.dependencies.authorization import get_api_key
from src.models import ApiKey
from src.schemas.design import (
    DesignCreate,
    DesignOut,
    DesignParamsCreate,
    DesignParamsInfo,
    DesignParamsOut
)

router = APIRouter(
    prefix="/designs",
    tags=["Designs"]
)


@router.post("/", response_model=DesignOut, status_code=status.HTTP_201_CREATED)
async def create_design(
    design_data: Annotated[DesignCreate, Depends()],
    api_key: Annotated[ApiKey, Depends(get_api_key)],
    session: Annotated[AsyncSession, Depends(get_session)]
):
    """Создание нового проекта"""

    new_design = await create_new_design(design_data, session)

    return new_design


@router.put("/{design_id}", response_model=DesignOut, status_code=status.HTTP_200_OK)
async def update_design(
    design_id: int,
    design_data: Annotated[DesignCreate, Depends()],
    api_key: Annotated[ApiKey, Depends(get_api_key)],
    session: Annotated[AsyncSession, Depends(get_session)]
):
    """Изменить проект"""

    design = await update_design_by_id(design_id=design_id, design_data=design_data, session=session)
    if design is None:
        raise HTTPException(status_code=404, detail="Design not found")

    return design


@router.get("/{design_id}", response_model=DesignOut, status_code=status.HTTP_200_OK)
async def get_design(
        design_id: int,
        api_key: Annotated[ApiKey, Depends(get_api_key)],
        session: Annotated[AsyncSession, Depends(get_session)]
):
    """Получить проект"""

    design = await get_design_by_id(design_id=design_id, session=session)
    if design is None:
        return HTTPException(status_code=404, detail="Design not found")

    return design


@router.post("/params/{design_id}", response_model=DesignParamsOut, status_code=status.HTTP_201_CREATED)
async def add_design_params(
        design_id: int,
        params_data: DesignParamsCreate,
        api_key: Annotated[ApiKey, Depends(get_api_key)],
        session: Annotated[AsyncSession, Depends(get_session)]
):
    """Создание нового проекта"""

    new_design_params = await create_design_params_by_design_id(design_id, params_data, session)

    return new_design_params


@router.put("/params/{design_id}", response_model=DesignParamsOut, status_code=status.HTTP_200_OK)
async def update_design_params(
        design_id: int,
        params_data: Annotated[DesignParamsCreate, Depends()],
        api_key: Annotated[ApiKey, Depends(get_api_key)],
        session: Annotated[AsyncSession, Depends(get_session)]
):
    """Изменить проект"""

    design_params = await update_design_params_by_design_id(
        design_id=design_id,
        params_data=params_data,
        session=session
    )
    if design_params is None:
        raise HTTPException(status_code=404, detail="Design params not found")

    return design_params


@router.get("/params/{design_id}", response_model=DesignParamsInfo, status_code=status.HTTP_200_OK)
async def get_design_params(
        design_id: int,
        api_key: Annotated[ApiKey, Depends(get_api_key)],
        session: Annotated[AsyncSession, Depends(get_session)]
):

    design_params = await get_design_info_by_design_id(design_id=design_id, session=session)
    if design_params is None:
        raise HTTPException(status_code=404, detail="Design params not found")

    return design_params

