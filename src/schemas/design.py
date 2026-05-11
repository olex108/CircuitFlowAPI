from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

from src.models.design import DesignType, Material


class DesignBase(BaseModel):
    name: str = Query(..., min_length=1, max_length=255, description="Название проекта")
    type: DesignType = Query(..., description="Тип недвижимости")
    address: Optional[str] = Query(None, description="Адрес объекта (полный или частичный)")
    square: int = Query(..., gt=0, description="Площадь в кв. метрах")


class DesignCreate(DesignBase):
    pass


class DesignOut(DesignBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_at: datetime


class DesignParamsBase(BaseModel):
    room_quantity: int = Query(default=1, ge=1, description="Указать с учетом кухни и учетом ванных комнат")
    walls_material: Material = Query(..., description="Материал несущих стен")
    partitions_material: Optional[Material] = Query(None, description="Материал перегородок")
    suspended_ceiling: bool = Query(default=True, description="Наличие натяжного потолка")

    # Количественные показатели
    sockets_quantity: Optional[int] = Query(None, ge=0, description="Розетки по количеству отверстий")
    switches_quantity: Optional[int] = Query(None, ge=0, description="Одноклавишные и двухклавишные суммарно")
    communication_sockets_quantity: Optional[int] = Query(None, ge=0, description="ТВ и интернет розетки")
    light_point_quantity: Optional[int] = Query(None, ge=0, description="Светильники, бра, подсветки")

    # Флаги оборудования
    built_box: bool = Query(default=False, description="Встроенный электрический щиток")
    power_cable: bool = Query(default=False, description="Замена вводного кабель")
    washing_machine: bool = Query(default=False, description="Стиральная машина")
    dishwasher: bool = Query(default=False, description="Посудомоечная машина")
    boiler: bool = Query(default=False, description="Бойлер")
    el_plate: bool = Query(default=False, description="Электрическая плита")
    water_heater: bool = Query(default=False, description="Водонагреватель")
    oven: bool = Query(default=False, description="Духовой шкаф")
    other_electric_appliance_quantity: int = Query(
        default=0,
        ge=0,
        description="Доп количество приборов (кондиционеры, нагреватели и т.п.)"
    )


class DesignParamsCreate(DesignParamsBase):
    """Схема для создания параметров"""

    pass


class DesignParamsInfo(DesignParamsBase):
    """Схема для возврата данных из API"""

    id: int
    design: DesignOut

    model_config = ConfigDict(from_attributes=True)


class DesignParamsOut(DesignParamsBase):
    """Схема для возврата данных из API"""

    id: int
    design_id: int

    model_config = ConfigDict(from_attributes=True)