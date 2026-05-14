import copy
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.calculations.parameters import price_list, circuit_breakers_list
from src.models.design import DesignParams, DesignType, Material
from src.models.estimate import EstimateStatus, Estimate
from src.schemas.estimate import EstimateInfo
from pydantic import BaseModel


# class EstimatePosition(BaseModel):
#     "Устройство отверстия под подрозетник (бетон)": 300,
#     "Устройство отверстия под подрозетник (газоблок)": 250,
#     "Устройство отверстия под подрозетник (гипсокартон)": 250,
#     "Штробление стен 20*20 (бетон)": 300,
#     "Штробление стен 20*20 (газоблок)": 250,
#     "Протяжка кабеля силового 3*6.0 / 5*2.5": 120,
#     "Протяжка кабеля силового 3*2.5": 100,
#     "Протяжка кабеля силового 3*1.5": 100,
#     "Протяжка кабеля слаботочного": 100,
#     "Монтаж и расключение распределительной коробки": 600,
#     "Монтаж подрозетника": 150,
#     "Монтаж, сборка и подключение щита силового (12мод)": 8000,
#     "Монтаж, сборка и подключение щита силового (24мод)": 12000,
#     "Монтаж, сборка и подключение щита силового (36мод)": 16000,
#     "Монтаж, сборка и подключение щита силового (48мод)": 20000,
#     "Устройство отверстия проходного (бетон)": 100,
#     "Устройство отверстия проходного (газоблок)": 50,
#     "Замена вводного кабеля": 5000,
#     "Устройство ниши под щит (12мод)": 4000,
#     "Устройство ниши под щит (24мод)": 6000,
#     "Устройство ниши под щит (36мод)": 8000,
#     "Устройство ниши под щит (48мод)": 10000,

class EstimateHandler:

    def __init__(self, estimate_info: EstimateInfo) -> None:
        self.estimate_info = estimate_info
        self.estimate_dict = {}
        self.estimate_price = {}
        self.circuit_breakers_project_list = {}

    def get_estimate_dict(self) -> dict:
        """Получить смету в форме словаря по заданным параметрам"""


    def calculate_estimate(self):
        """
        Функция создает смету из параметров проекта

        Запись параметров сметы в словарь:: осуществляется путем составления из разных параметров проекта

        Расчет количества отверстий под подрозетники:: складывание количества розеток и выключателей

        Расчет количества штробы:: путем составления умножения количества розеток и выключателей на соответствующие
        коэффициенты, полученные эмпирическим путем !!!!! Требует пересмотра !!!!!

        Расчет количества кабеля:: путем составления умножения количества розеток на соответствующее количество и
        дополнительных линий на приборы. Полученный результат умножается на коэффициент, полученные путем учета различных
        параметров объекта !!!!! Требует доработки !!!!!

        Расчет количества монтируемых подрозетников:: с количества отверстий под подрозетники

        Замена вводного кабеля:: добавляется в зависимости соответствующего от параметра объекта

        Расчет количества автоматов для щита:: часть функции для определения количества автоматов с учетом типа проекта
        и определения типоразмера щита

        Устройство ниши под щит:: добавляется в зависимости соответствующего от параметра объекта

        """

        # Запись параметров сметы в словарь
        # self.estimate_dict["Название проекта"] = self.estimate_info.design_params.design.name
        # self.estimate_dict["Список работ"] = "До замера"
        # self.estimate_dict["Тип"] = f"{self.estimate_info.design_params.design.type}"
        # self.estimate_dict["Площадь помещения"] = f"{self.estimate_info.design_params.design.square}м2"

        # Расчет количества отверстий под подрозетники:
        socket_key = f"Устройство отверстия под подрозетник ({self.estimate_info.design_params.walls_material})"
        socket_count = (self.estimate_info.design_params.sockets_quantity +
                        self.estimate_info.design_params.switches_quantity +
                        self.estimate_info.design_params.communication_sockets_quantity)


        socket_price = socket_count * price_list[socket_key]
        # Записываем позицию в смету по параметрам: количество, тариф, стоимость
        if self.estimate_info.design_params.walls_material == self.estimate_info.design_params.partitions_material:
            self.estimate_price[
                socket_key] = f"{socket_count}шт * {price_list[socket_key]} = {socket_price}руб."
        else:
            self.estimate_price[socket_key] = (
                f"{round(socket_count * 0.7)}шт * {price_list[socket_key]} = "
                f"{round(socket_count * 0.7) * price_list[socket_key]}руб."
            )
            socket_key = f"Устройство отверстия под подрозетник ({self.estimate_info.design_params.partitions_material})"
            self.estimate_price[socket_key] = (
                f"{round(socket_count * 0.3)}шт * {price_list[socket_key]} = "
                f"{round(socket_count * 0.3) * price_list[socket_key]}руб."
            )

        # Расчет количества штробы:
        groove_coefficient = 1
        if self.estimate_info.design_params.suspended_ceiling:
            groove_coefficient *= 2
        if self.estimate_info.design_params.design.square > 80:
            groove_coefficient *= 1.2
        if self.estimate_info.design_params.design.square > 140:
            groove_coefficient *= 1.2
        if self.estimate_info.design_params.design.type == DesignType.HOUSE or self.estimate_info.design_params.design.type == DesignType.COMMERCIAL:
            groove_coefficient *= 1.2
        groove_count = round(
            (
                    self.estimate_info.design_params.sockets_quantity * 1.2 +
                    self.estimate_info.design_params.switches_quantity * 1.5 +
                    self.estimate_info.design_params.communication_sockets_quantity * 1.5
            )
            * groove_coefficient
        )
        if self.estimate_info.design_params.walls_material != Material.PLASTERBOARD:
            groove_key = f"Штробление стен 20*20 ({self.estimate_info.design_params.walls_material})"
            groove_price = groove_count * price_list[groove_key]
            # Записываем позицию в смету по параметрам: количество, тариф, стоимость
            if self.estimate_info.design_params.walls_material == self.estimate_info.design_params.partitions_material:
                self.estimate_price[groove_key] = (
                    f"{groove_count}м.п. * {price_list[groove_key]} = {groove_price}руб"
                )
            else:
                self.estimate_price[groove_key] = (
                    f"{round(groove_count * 0.7)}м.п. * {price_list[groove_key]} = "
                    f"{round(groove_count * 0.7) * price_list[groove_key]}руб"
                )
                if (
                    self.estimate_info.design_params.partitions_material != Material.PLASTERBOARD
                    and
                    self.estimate_info.design_params.walls_material != self.estimate_info.design_params.partitions_material
                ):
                    groove_key = f"Штробление стен 20*20 ({self.estimate_info.design_params.partitions_material})"
                    self.estimate_price[groove_key] = (
                        f"{round(groove_count * 0.3)}м.п. * {price_list[groove_key]} = "
                        f"{round(groove_count * 0.3) * price_list[groove_key]}руб"
                    )

        # Расчет количества кабеля:
        cable_coefficient = 1
        if self.estimate_info.design_params.suspended_ceiling:
            cable_coefficient *= 2
        if self.estimate_info.design_params.design.square > 80:
            cable_coefficient *= 1.2
        if self.estimate_info.design_params.design.square > 140:
            cable_coefficient *= 1.2
        if self.estimate_info.design_params.design.type == DesignType.HOUSE or self.estimate_info.design_params.design.type == DesignType.COMMERCIAL:
            cable_coefficient *= 1.2
        # 5*2,5 / 3*6
        cable_count = 0
        if self.estimate_info.design_params.el_plate:
            cable_count += 15
        if self.estimate_info.design_params.water_heater:
            cable_count += 15
        if cable_count != 0:
            cable_count *= cable_coefficient
            self.estimate_price["Протяжка кабеля силового 3*6.0 / 5*2.5"] = (
                f"{round(cable_count)}м.п. * {price_list["Протяжка кабеля силового 3*6.0 / 5*2.5"]} = "
                f"{round(cable_count) * price_list["Протяжка кабеля силового 3*6.0 / 5*2.5"]}руб"
            )
        # 3*2,5
        cable_for_socket_coefficient = cable_coefficient
        if socket_count / self.estimate_info.design_params.design.square > 1.4:
            cable_for_socket_coefficient = cable_coefficient * 1.4
        cable_count = self.estimate_info.design_params.room_quantity * 30
        if self.estimate_info.design_params.washing_machine:
            cable_count += 10
        if self.estimate_info.design_params.dishwasher:
            cable_count += 10
        if self.estimate_info.design_params.boiler:
            cable_count += 10
        if self.estimate_info.design_params.oven:
            cable_count += 10

        cable_count += self.estimate_info.design_params.other_electric_appliance_quantity * 10
        cable_count *= cable_for_socket_coefficient

        self.estimate_price["Протяжка кабеля силового 3*2.5"] = (
            f"{round(cable_count, -1)}м.п. * {price_list["Протяжка кабеля силового 3*2.5"]} = "
            f"{round(cable_count, -1) * price_list["Протяжка кабеля силового 3*2.5"]}руб"
        )
        # 3*1,5
        cable_for_light_coefficient = cable_coefficient
        if self.estimate_info.design_params.light_point_quantity / self.estimate_info.design_params.room_quantity > 2:
            cable_for_light_coefficient = cable_coefficient * 1.4
        if self.estimate_info.design_params.switches_quantity / self.estimate_info.design_params.room_quantity > 2.5:
            cable_for_light_coefficient = cable_coefficient * 1.4
        cable_count = self.estimate_info.design_params.room_quantity * 20 * cable_for_light_coefficient
        self.estimate_price["Протяжка кабеля силового 3*1.5"] = (
            f"{round(cable_count, -1)}м.п. * {price_list["Протяжка кабеля силового 3*1.5"]} = "
            f"{round(cable_count, -1) * price_list["Протяжка кабеля силового 3*1.5"]}руб"
        )

        # Расчет количества монтируемых подрозетников:
        self.estimate_price["Монтаж подрозетника"] = (
            f"{socket_count}шт * {price_list["Монтаж подрозетника"]} = "
            f"{socket_count * price_list["Монтаж подрозетника"]}руб."
        )

        # Расчет количества отверстий:

        # Замена вводного кабеля:
        if self.estimate_info.design_params.power_cable:
            self.estimate_price["Замена вводного кабеля"] = (
                f" 1шт * {price_list["Замена вводного кабеля"]} = "
                f"{price_list["Замена вводного кабеля"]}руб."
            )

        # Расчет количества автоматов для щита:
        module_counter = 0
        self.circuit_breakers_project_list = copy.deepcopy(circuit_breakers_list)

        if self.estimate_info.design_params.design == DesignType.HOUSE:
            self.circuit_breakers_project_list["Рубильник реверсивный"] = 1
            module_counter += 4
            self.circuit_breakers_project_list["Вводное УЗО"] = 1
            module_counter += 4
            self.circuit_breakers_project_list["Влагозащитное УЗО"] = 2
            module_counter += 4
            self.circuit_breakers_project_list["Уличное УЗО"] = 1
            module_counter += 2
            self.circuit_breakers_project_list["Автомат большой мощности"] = sum(
                [
                    self.estimate_info.design_params.el_plate,
                    self.estimate_info.design_params.water_heater,
                ]
            )
            module_counter += 3 * self.circuit_breakers_project_list["Автомат большой мощности"]

        elif self.estimate_info.design_params.design == DesignType.APARTMENT:
            self.circuit_breakers_project_list["Рубильник реверсивный"] = 0
            self.circuit_breakers_project_list["Вводное УЗО"] = 1
            module_counter += 2
            self.circuit_breakers_project_list["Влагозащитное УЗО"] = 1
            module_counter += 2
            self.circuit_breakers_project_list["Уличное УЗО"] = 0
            self.circuit_breakers_project_list["Автомат большой мощности"] = sum(
                [
                    self.estimate_info.design_params.el_plate,
                    self.estimate_info.design_params.water_heater,
                ]
            )
            module_counter += self.circuit_breakers_project_list["Автомат большой мощности"]

        self.circuit_breakers_project_list["Дифференциальный автомат 16А 30мА"] = sum(
            [
                self.estimate_info.design_params.washing_machine,
                self.estimate_info.design_params.dishwasher,
                self.estimate_info.design_params.boiler,
            ]
        )
        module_counter += 2 * self.circuit_breakers_project_list["Дифференциальный автомат 16А 30мА"]

        self.circuit_breakers_project_list["Автомат 16А"] = sum(
            [
                self.estimate_info.design_params.room_quantity + 1,
                self.estimate_info.design_params.oven,
                self.estimate_info.design_params.other_electric_appliance_quantity,
            ]
        )
        module_counter += self.circuit_breakers_project_list["Автомат 16А"]

        self.circuit_breakers_project_list["Автомат 10А"] = (self.estimate_info.design_params.room_quantity + 1) // 2
        module_counter += self.circuit_breakers_project_list["Автомат 10А"]

        if self.estimate_info.design_params.design == DesignType.PARTIAL:
            self.estimate_price["Количество дополнительных автоматов"] = "По результатам замера"
        else:
            switch_box_modules = (module_counter // 12 + 1) * 12 if module_counter < 48 else 48
            switch_box_key = f"Монтаж, сборка и подключение щита силового ({switch_box_modules}мод)"
            self.estimate_price[switch_box_key] = (
                f"1шт * {price_list[switch_box_key]} = " f"{price_list[switch_box_key]} руб."
            )

            # Устройство ниши под щит:
            if self.estimate_info.design_params.built_box:
                switch_box_key = f"Устройство ниши под щит ({switch_box_modules}мод)"
                self.estimate_price[switch_box_key] = (
                    f" 1шт * {price_list[switch_box_key]} = " f"{price_list[switch_box_key]}руб."
                )

        return self.estimate_price

