from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import datetime

from src.models.estimate import EstimateStatus


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

    model_config = ConfigDict(from_attributes=True)
    message: str = "Проект отправлен на расчет"


class EstimateOut(EstimateBase):

    model_config = ConfigDict(from_attributes=True)
