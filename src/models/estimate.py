from datetime import datetime
from enum import Enum
import random

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLEnum, func, ForeignKey, JSON, text

from src.models.base import BaseModel

def generate_8_digit_id():
    # Генерирует число от 10 000 000 до 99 999 999
    return random.randint(10000000, 99999999)


class EstimateStatus(str, Enum):
    CREATED = "создана"
    COMPLEAT = "просчитана"
    ERROR = "ошибка"


class Estimate(BaseModel):

    __tablename__ = "estimates"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        default=generate_8_digit_id
    )
    design_params_id: Mapped[int] = mapped_column(ForeignKey("design_params.id", ondelete="CASCADE"))
    create_at: Mapped[datetime] = mapped_column(server_default=func.now(), default=func.now())
    status: Mapped[EstimateStatus] = mapped_column(
        SQLEnum(EstimateStatus, name="status"),
        nullable=False,
        default=EstimateStatus.CREATED
    ),
    error: Mapped[str] = mapped_column(nullable=True)
    estimate: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,              # Делаем поле обязательным (не null)
        default=lambda: {},          # Для генерации на стороне Python (при добавлении через ORM)
        server_default=text("'{}'")  # Для генерации на стороне самой БД (SQLite/Postgres)
    )

    # Обратные связи
    design_params: Mapped["DesignParams"] = relationship(back_populates="estimates")
