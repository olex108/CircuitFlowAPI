from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.design import DesignParams
from src.models.estimate import EstimateStatus, Estimate


class EstimateHandler:

    def __init__(self, estimate: Estimate) -> None:
        self.estimate = estimate
        # Больше не вызываем асинхронный код в init
        self.design_params: Optional[DesignParams] = None

    async def initialize(self, session: AsyncSession) -> bool:
        """
        Асинхронная инициализация хэндлера.
        Загружает параметры дизайна и обновляет статус при ошибке.
        """
        self.design_params = await self.get_design_params(session)

        if self.design_params is None:
            self.estimate.status = EstimateStatus.ERROR
            self.estimate.error = "Get design params error"
            await self.save_estimate(self.estimate, session)
            return False

        return True

    async def get_design_params(self, session: AsyncSession) -> Optional[DesignParams]:
        # Сессию ОБЯЗАТЕЛЬНО передаем аргументом из эндпоинта или воркера Taskiq
        query = select(DesignParams).where(DesignParams.id == self.estimate.design_params_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def save_estimate(self, estimate: Estimate, session: AsyncSession) -> Estimate:
        session.add(estimate)  # Гарантируем, что объект привязан к текущей сессии
        await session.commit()
        await session.refresh(estimate)
        return estimate  # Теперь вернет обновленный объект, а не None
