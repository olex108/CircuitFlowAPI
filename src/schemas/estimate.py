from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import datetime

from src.models.estimate import EstimateStatus
from src.schemas.design import DesignParamsInfo


class EstimateBase(BaseModel):

    id: int
    design_params_id: int
    create_at: datetime
    estimate: dict
    status: EstimateStatus = EstimateStatus.CREATED
    error: str | None = None


class EstimateCreate(EstimateBase):
    pass


class EstimateCreated(EstimateBase):
    """Схема для возвращения созданной новой сметы"""

    model_config = ConfigDict(from_attributes=True)
    message: str = "Проект отправлен на расчет"


class EstimateOut(EstimateBase):
    """Схема возвращения сметы"""

    model_config = ConfigDict(from_attributes=True)


class EstimateInfo(EstimateBase):
    """Схема для хранения всей информации о смете, параметрам проекта"""

    design_params: DesignParamsInfo

    model_config = ConfigDict(from_attributes=True)
