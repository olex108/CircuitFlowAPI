from certifi import where
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.schemas.design import DesignCreate, DesignParamsCreate, DesignParamsOut
from src.models.design import Design, DesignParams


async def create_new_design(design_data: DesignCreate, session: AsyncSession) -> Design:
    new_design = Design(**design_data.model_dump())

    session.add(new_design)
    await session.commit()
    await session.refresh(new_design)

    return new_design


async def update_design_by_id(design_id: int, design_data: DesignCreate, session: AsyncSession) -> Design | None:

    db_design = await session.get(Design, design_id)
    if db_design is None:
        return None
    db_design.name = design_data.name
    db_design.type = design_data.type
    db_design.address = design_data.address
    db_design.square = design_data.square

    try:
        await session.commit()
        db_design = await session.refresh(db_design)
    except Exception:
        return None

    return db_design


async def get_design_by_id(design_id: int, session: AsyncSession) -> Design | None:
    query = select(Design).where(Design.id == design_id)
    result = (await session.execute(query)).scalar_one_or_none()
    return result


async def create_design_params_by_design_id(
        design_id: int,
        params_data: DesignParamsCreate,
        session: AsyncSession
) -> DesignParams | None:

    # Проверка существует ли объект с design_id
    db_design_params = session.get(DesignParams, design_id)
    if db_design_params:
        return None

    new_design_params = DesignParams(
        design_id=design_id,
        **params_data.model_dump()
    )
    session.add(new_design_params)
    try:
        await session.commit()
        await session.refresh(new_design_params)
    except Exception as ex:
        print(ex)
        await session.rollback()
        return None
    return new_design_params


async def update_design_params_by_design_id(
        design_id: int,
        params_data: DesignParamsCreate,
        session: AsyncSession
) -> DesignParams | None:

    db_design_params = session.get(DesignParams, design_id)
    if db_design_params is None:
        return None

    update_data = params_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_design_params, key, value)

    try:
        await session.commit()
        design_params = await session.refresh(db_design_params)
    except Exception as ex:
        print(ex)
        await session.rollback()
        return None
    return design_params


async def get_design_info_by_design_id(design_id: int, session: AsyncSession) -> DesignParams | None:
    query = select(DesignParams).where(DesignParams.design_id == design_id).options(selectinload(DesignParams.design))
    result = (await session.execute(query)).scalar_one_or_none()
    return result
