from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from src.calculations.estimate import EstimateHandler
from src.config.broker_taskiq import broker
from src.config.database import get_session
from src.models import Estimate
from src.crud.estimate import get_estimate_info_by_id, save_estimate_in_db

from taskiq import TaskiqDepends

from src.models.estimate import EstimateStatus
from src.schemas.estimate import EstimateInfo


@broker.task
async def calculate_estimate_save_in_db(
        estimate_id: int,
        session: Annotated[AsyncSession, TaskiqDepends(get_session)]
) -> None:
    """Отложенная задача для вызова расчета сметы и записи в базу данных.
    Получения полной информации о заказе.
    Получение результатов расчета сметы
    Сохранение результатов расчета сметы в базу данных
    """

    estimate_db: Estimate = await get_estimate_info_by_id(estimate_id=estimate_id, session=session)
    estimate = EstimateHandler(EstimateInfo.model_validate(estimate_db))
    try:
        estimate_db.estimate = estimate.calculate_estimate()
        estimate_db.status = EstimateStatus.COMPLEAT
        await save_estimate_in_db(estimate_db, session)
    except Exception as ex:
        estimate_db.status = EstimateStatus.ERROR
        estimate_db.error = str(ex.args)
        await save_estimate_in_db(estimate_db, session)
