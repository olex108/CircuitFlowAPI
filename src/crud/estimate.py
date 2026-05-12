from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.estimate import Estimate


async def create_estimate_for_design_params(design_params_id: int, session: AsyncSession) -> Estimate | None:
    new_estimate = Estimate(
        design_params_id=design_params_id
    )
    session.add(new_estimate)
    try:
        await session.commit()
        await session.refresh(new_estimate)

    except Exception as ex:
        print(ex)
        await session.rollback()
        return None

    return new_estimate

async def get_estimate_by_id(estimate_id: int, session: AsyncSession) -> Estimate | None:

    query = select(Estimate).where(Estimate.id == estimate_id)
    result = (await session.execute(query)).scalar_one_or_none()
    return result
