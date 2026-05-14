from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_session
from src.dependencies.authorization import get_api_key
from src.models import ApiKey

from src.crud.estimate import create_estimate_for_design_params, get_estimate_by_id
from src.schemas.estimate import EstimateOut, EstimateCreated

router = APIRouter(
    prefix="/estimates",
    tags=["Estimates"]
)


@router.post("/{design_params_id}", response_model=EstimateCreated , status_code=status.HTTP_201_CREATED)
async def create_estimate(
        design_params_id: int,
        api_key: Annotated[ApiKey, Depends(get_api_key)],
        session: Annotated[AsyncSession, Depends(get_session)]
):
    """Создать смету для design_params_id"""

    estimate = await create_estimate_for_design_params(design_params_id=design_params_id, session=session)

    if estimate is None:
        raise HTTPException(
            status_code=status.HTTP_404_BAD_REQUEST,
            detail="Design params is not found"
        )

    return estimate


@router.get("/{estimate_id}", response_model=EstimateOut, status_code=status.HTTP_200_OK)
async def get_estimate(
        estimate_id: int,
        api_key: Annotated[ApiKey, Depends(get_api_key)],
        session: Annotated[AsyncSession, Depends(get_session)]
):
    """Получить смету по id"""

    estimate = await get_estimate_by_id(estimate_id=estimate_id, session=session)

    if estimate is None:
        raise HTTPException(
            status_code=status.HTTP_404_BAD_REQUEST,
            detail="Estimate is not found"
        )

    return estimate
