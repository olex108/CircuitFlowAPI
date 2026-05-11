from datetime import datetime
from enum import Enum
import random
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLEnum, func, ForeignKey

from src.models.base import BaseModel


def generate_8_digit_id():
    # Генерирует число от 10 000 000 до 99 999 999
    return random.randint(10000000, 99999999)


class DesignType(str, Enum):
    """Тип проекта"""

    HOUSE = "дом"
    APARTMENT = "квартира"
    COMMERCIAL = "коммерция"
    PARTIAL = "частичная (комната/кухня)"


class Material(str, Enum):
    """Материал стен и перегородок"""

    CONCRETE = "бетон"
    AERATE = "газоблок"
    PLASTERBOARD = "гипсокартон"


class Design(BaseModel):

    __tablename__ = "designs"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        default=generate_8_digit_id
    )

    name: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[DesignType] = mapped_column(
        SQLEnum(DesignType, name="design_type"),
        nullable=False,
    )
    address: Mapped[str] = mapped_column(nullable=True)
    square: Mapped[int] = mapped_column(nullable=False)

    create_at: Mapped[datetime] = mapped_column(server_default=func.now(), default=func.now())

    # Обратные связи
    design_params: Mapped["DesignParams"] = relationship(back_populates="design")


class DesignParams(BaseModel):

    __tablename__ = "design_params"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        default=generate_8_digit_id
    )

    design_id: Mapped[int] = mapped_column(ForeignKey("designs.id", ondelete="CASCADE"), unique=True)

    room_quantity: Mapped[int] = mapped_column(default=1, nullable=False) # "Указать с учетом кухни и учетом ванных комнат",
    walls_material: Mapped[Material] = mapped_column(
        SQLEnum(Material, name="walls_material"),
        nullable=False,
    )
    partitions_material: Mapped[Material] = mapped_column(
        SQLEnum(Material, name="walls_material"),
        nullable=True,
    )
    suspended_ceiling: Mapped[bool] = mapped_column(nullable=False, default=True)
    sockets_quantity: Mapped[int] = mapped_column(nullable=True) # Указать розетки по количеству отверстий
    switches_quantity: Mapped[int] = mapped_column(nullable=True) # Указать количество вместе одноклавишных и двухклавишных
    communication_sockets_quantity: Mapped[int] = mapped_column(nullable=True) # Указать ТВ и интернет розетки по количеству отверстий
    light_point_quantity: Mapped[int] = mapped_column(nullable=True) # Светильники, группа точечных светильников, бра, подсветки
    built_box: Mapped[bool] = mapped_column(default=False) # Встроенный/Наружный
    power_cable: Mapped[bool] = mapped_column(default=False)
    washing_machine: Mapped[bool] = mapped_column(default=False)
    dishwasher : Mapped[bool] = mapped_column(default=False)
    boiler: Mapped[bool] = mapped_column(default=False)
    el_plate: Mapped[bool] = mapped_column(default=False)
    water_heater: Mapped[bool] = mapped_column(default=False)
    oven: Mapped[bool] = mapped_column(default=False)
    other_electric_appliance_quantity: Mapped[int] = mapped_column(default=0) # Количество приборов

    # Обратные связи
    design: Mapped["Design"] = relationship(back_populates="design_params")
    estimates: Mapped[List["Estimate"]] = relationship(back_populates="design_params")
