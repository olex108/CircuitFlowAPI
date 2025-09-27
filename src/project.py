from typing import Any

from src.electric_line import ElectricLine
from src.file_handler import JSONHandler

from config import PATH_TO_PRICE


class Project(object):
    """Class of project"""

    __project_name: str
    __project_address: str
    __project_square: int
    __project_type: str
    __electric_lines_list: list[ElectricLine]
    __project_params: dict
    __project_estimate_params: dict

    def __init__(self, project_name, project_address, project_square, project_type):
        """

        :param project_name:
        :param project_address:
        :param project_square:
        :param project_type:
        """

        self.__project_name = project_name
        self.__project_address = project_address
        self.__project_square = project_square
        self.__project_type = project_type
        self.__electric_lines_list = []
        self.__project_params = {}
        self.__project_estimate_params = {}
        self.__electric_box = {}

    @classmethod
    def create_new_project(cls, new_project_dict: dict) -> Any:
        """
        Create new project from given dict.

            project_name_parameters = {
                "project_name": "Адрес или имя(запомните)",
                "address": "Полный либо частичный адрес",
                "project_type": ["квартира", "дом", "коммерция", "частичная (комната/кухня)"],
                "square": "м2",
            }
            """

        try:
            project_name = new_project_dict.get("project_name")
            project_address = new_project_dict.get("project_address")
            project_square = new_project_dict.get("project_square")
            project_type = new_project_dict.get("project_type")
            return cls(project_name, project_address, project_square, project_type)

        except KeyError as e:
            print(e)
            return None

    def add_project_params(self, project_params: dict) -> None:
        """
        Method for verification add change project_params.
        Take dict of project params

            project_parameters = {
                "room_quantity": "Указать с учетом кухни и учетом ванных комнат",
                "walls_material": ["Бетон", "Газоблок", "Гипсокартон"],
                "partitions_material": ["Бетон", "Газоблок", "Гипсокартон"],
                "ceiling_material": "Да/нет",
                "sockets_quantity": "Указать розетки по количеству отверстий",
                "switches_quantity": "Указать количество вместе одноклавишных и двухклавишных",
                "communication_sockets_quantity": "Указать ТВ и интернет розетки по количеству отверстий",
                "light_point_quantity": "Светильники, группа точечных светильников, бра, подсветки",
                "electrical_box": "Встроенный/Наружный",
                "power_cable": "Да/нет",
                "washing_machine": "Да/нет",
                "dishwasher": "Да/нет",
                "boiler": "Да/нет",
                "el_plate": "Да/нет",
                "water_heater": "Да/нет",
                "oven": "Да/нет",
                "other_electric_appliance_quantity": Количество приборов,
            }

        """

        new_project_params = {}

        print()
        try:
            # new_project_params["room_quantity"] = project_params["room_quantity"]
            # new_project_params["walls_material"] = project_params["walls_material"]
            # new_project_params["partitions_material"] = project_params["partitions_material"]
            # new_project_params["ceiling_material"] = project_params["ceiling_material"]
            # new_project_params["sockets_quantity"] = project_params["sockets_quantity"]
            # new_project_params["switches_quantity"] = project_params["switches_quantity"]
            # new_project_params["communication_sockets_quantity"] = project_params["communication_sockets_quantity"]
            # new_project_params["light_point_quantity"] = project_params["light_point_quantity"]
            # new_project_params["electrical_box"] = project_params["electrical_box"]
            # new_project_params["power_cable"] = project_params["power_cable"]
            # new_project_params["washing_machine"] = project_params["washing_machine"]
            # new_project_params["dishwasher"] = project_params["dishwasher"]
            # new_project_params["boil"] = project_params["boil"]
            # new_project_params["el_plate"] = project_params["el_plate"]
            # new_project_params["water_heater"] = project_params["water_heater"]
            # new_project_params["oven"] = project_params["oven"]
            # new_project_params["other_electric_appliance_quantity"] = project_params["other_electric_appliance_quantity"]
            #
            new_project_params["room_quantity"] = project_params.get("room_quantity")
            new_project_params["walls_material"] = project_params.get("walls_material")
            new_project_params["partitions_material"] = project_params.get("partitions_material")
            new_project_params["ceiling_material"] = project_params.get("ceiling_material")
            new_project_params["sockets_quantity"] = project_params.get("sockets_quantity")
            new_project_params["switches_quantity"] = project_params.get("switches_quantity")
            new_project_params["communication_sockets_quantity"] = project_params.get("communication_sockets_quantity")
            new_project_params["light_point_quantity"] = project_params.get("light_point_quantity")
            new_project_params["electrical_box"] = project_params.get("electrical_box")
            new_project_params["power_cable"] = project_params.get("power_cable")
            new_project_params["washing_machine"] = project_params.get("washing_machine")
            new_project_params["dishwasher"] = project_params.get("dishwasher")
            new_project_params["boiler"] = project_params.get("boiler")
            new_project_params["el_plate"] = project_params.get("el_plate")
            new_project_params["water_heater"] = project_params.get("water_heater")
            new_project_params["oven"] = project_params.get("oven")
            new_project_params["other_electric_appliance_quantity"] = project_params.get("other_electric_appliance_quantity")

            self.__project_params = new_project_params

        except KeyError as e:
            print(e)

    def get_estimate_by_project_params(self) -> dict:
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

        # Создаем словарь для записи пунктов сметы
        project_estimate = {}

        price = JSONHandler(PATH_TO_PRICE).get_data()

        # Запись параметров сметы в словарь
        project_estimate["Название проекта"] = self.__project_name
        project_estimate["Адрес объекта"] = self.__project_address
        project_estimate["Список работ"] = "До замера"
        project_estimate[
            "Объект:"] = f"{self.__project_type}, {self.__project_square}м2"

        # Расчет количества отверстий под подрозетники:
        socket_key = f"Устройство отверстия под подрозетник ({self.__project_params["walls_material"].lower()})"
        socket_count = (
                int(self.__project_params["sockets_quantity"])
                + int(self.__project_params["switches_quantity"])
                + int(self.__project_params["communication_sockets_quantity"])
        )
        socket_price = socket_count * price[socket_key]
        # Записываем позицию в смету по параметрам: количество, тариф, стоимость
        if self.__project_params["walls_material"].lower() == self.__project_params["partitions_material"].lower():
            project_estimate[
                socket_key] = f"{socket_count}шт * {price[socket_key]} = {socket_price}руб."
        else:
            project_estimate[socket_key] = (
                f"{round(socket_count * 0.7)}шт * {price[socket_key]} = "
                f"{round(socket_count * 0.7) * price[socket_key]}руб."
            )
            socket_key = f"Устройство отверстия под подрозетник ({self.__project_params["Материал перегородок"].lower()})"
            project_estimate[socket_key] = (
                f"{round(socket_count * 0.3)}шт * {price[socket_key]} = "
                f"{round(socket_count * 0.3) * price[socket_key]}руб."
            )

        # Расчет количества штробы:
        groove_coefficient = 1
        if self.__project_params["ceiling_material"] == "Да":
            groove_coefficient *= 2
        if int(self.__project_square) > 80:
            groove_coefficient *= 1.2
        if int(self.__project_square) > 140:
            groove_coefficient *= 1.2
        if self.__project_type == "дом" or self.__project_type == "коммерция":
            groove_coefficient *= 1.2
        groove_count = round(
            (
                    int(self.__project_params["sockets_quantity"]) * 1.2
                    + int(self.__project_params["switches_quantity"]) * 1.5
                    + int(self.__project_params["communication_sockets_quantity"]) * 1.5
            )
            * groove_coefficient
        )
        if self.__project_params["walls_material"].lower() != "гипсокартон":
            groove_key = f"Штробление стен 20*20 ({self.__project_params["walls_material"].lower()})"
            groove_price = groove_count * price[groove_key]
            # Записываем позицию в смету по параметрам: количество, тариф, стоимость
            if self.__project_params["walls_material"].lower() == self.__project_params["partitions_material"].lower():
                project_estimate[groove_key] = (
                    f"{groove_count}м.п. * {price[groove_key]} = {groove_price}руб"
                )
            else:
                project_estimate[groove_key] = (
                    f"{round(groove_count * 0.7)}м.п. * {price[groove_key]} = "
                    f"{round(groove_count * 0.7) * price[groove_key]}руб"
                )
                if (
                        self.__project_params["partitions_material"].lower() != "Гипсокартон"
                        and self.__project_params["walls_material"].lower() != self.__project_params[
                    "partitions_material"].lower()
                ):
                    groove_key = f"Штробление стен 20*20 ({self.__project_params["partitions_material"].lower()})"
                    project_estimate[groove_key] = (
                        f"{round(groove_count * 0.3)}м.п. * {price[groove_key]} = "
                        f"{round(groove_count * 0.3) * price[groove_key]}руб"
                    )

        # Расчет количества кабеля:
        cable_coefficient = 1
        if self.__project_params["ceiling_material"] == "Да":
            cable_coefficient *= 1.2
        if int(self.__project_square) > 80:
            cable_coefficient *= 1.2
        if int(self.__project_square) > 140:
            cable_coefficient *= 1.2
        if self.__project_type == "дом" or self.__project_type == "коммерция":
            cable_coefficient *= 1.2
        # 5*2,5 / 3*6
        cable_count = 0
        if self.__project_params["el_plate"] == "Да":
            cable_count += 15
        if self.__project_params["water_heater"] == "Да":
            cable_count += 15
        if cable_count != 0:
            cable_count *= cable_coefficient
            project_estimate["Протяжка кабеля силового 3*6.0 / 5*2.5"] = (
                f"{round(cable_count)}м.п. * {price["Протяжка кабеля силового 3*6.0 / 5*2.5"]} = "
                f"{round(cable_count) * price["Протяжка кабеля силового 3*6.0 / 5*2.5"]}руб"
            )
        # 3*2,5
        cable_for_socket_coefficient = cable_coefficient
        if (int(self.__project_params["sockets_quantity"]) / int(self.__project_square)) > 1.4:
            cable_for_socket_coefficient = cable_coefficient * 1.4
        cable_count = int(self.__project_params["room_quantity"]) * 30
        if self.__project_params["washing_machine"] == "Да":
            cable_count += 10
        if self.__project_params["dishwasher"] == "Да":
            cable_count += 10
        if self.__project_params["boiler"] == "Да":
            cable_count += 10
        if self.__project_params["oven"] == "Да":
            cable_count += 10

        cable_count += int(self.__project_params["other_electric_appliance_quantity"]) * 10
        print(cable_count)
        cable_count *= cable_for_socket_coefficient

        project_estimate["Протяжка кабеля силового 3*2.5"] = (
            f"{round(cable_count, -1)}м.п. * {price["Протяжка кабеля силового 3*2.5"]} = "
            f"{round(cable_count, -1) * price["Протяжка кабеля силового 3*2.5"]}руб"
        )
        # 3*1,5
        cable_for_light_coefficient = cable_coefficient
        if (int(self.__project_params["light_point_quantity"]) / int(self.__project_params["room_quantity"])) > 2:
            cable_for_light_coefficient = cable_coefficient * 1.4
        if (int(self.__project_params["switches_quantity"]) / int(self.__project_params["room_quantity"])) > 2.5:
            cable_for_light_coefficient = cable_coefficient * 1.4
        cable_count = int(self.__project_params["room_quantity"]) * 20 * cable_for_light_coefficient
        project_estimate["Протяжка кабеля силового 3*1.5"] = (
            f"{round(cable_count, -1)}м.п. * {price["Протяжка кабеля силового 3*1.5"]} = "
            f"{round(cable_count, -1) * price["Протяжка кабеля силового 3*1.5"]}руб"
        )

        # Расчет количества монтируемых подрозетников:
        project_estimate["Монтаж подрозетника"] = (
            f"{socket_count}шт * {price["Монтаж подрозетника"]} = "
            f"{socket_count * price["Монтаж подрозетника"]}руб."
        )

        # Расчет количества отверстий:

        # Замена вводного кабеля:
        if self.__project_params["power_cable"] == "Да":
            project_estimate["Замена вводного кабеля"] = (
                f" 1шт * {price["Замена вводного кабеля"]} = "
                f"{price["Замена вводного кабеля"]}руб."
            )

        # Расчет количества автоматов для щита:
        module_counter = 0

        if self.__project_type == "дом":
            self.__electric_box["Рубильник реверсивный"] = 1
            module_counter += 4
            self.__electric_box["Вводное УЗО"] = 1
            module_counter += 4
            self.__electric_box["Влагозащитное УЗО"] = 2
            module_counter += 4
            self.__electric_box["Уличное УЗО"] = 1
            module_counter += 2
            self.__electric_box["Автомат большой мощности"] = sum(
                [
                    self.__project_params["el_plate"] == "Да",
                    self.__project_params["water_heater"] == "Да",
                ]
            )
            module_counter += 3 * self.__electric_box["Автомат большой мощности"]

        elif self.__project_type == "квартира":
            self.__electric_box["Рубильник реверсивный"] = 0
            self.__electric_box["Вводное УЗО"] = 1
            module_counter += 2
            self.__electric_box["Влагозащитное УЗО"] = 1
            module_counter += 2
            self.__electric_box["Уличное УЗО"] = 0
            self.__electric_box["Автомат большой мощности"] = sum(
                [
                    self.__project_params["el_plate"] == "Да",
                    self.__project_params["water_heater"] == "Да",
                ]
            )
            module_counter += self.__electric_box["Автомат большой мощности"]

        self.__electric_box["Дифференциальный автомат 16А 30мА"] = sum(
            [
                self.__project_params["washing_machine"] == "Да",
                self.__project_params["dishwasher"] == "Да",
                self.__project_params["boiler"] == "Да",
            ]
        )
        module_counter += 2 * self.__electric_box["Дифференциальный автомат 16А 30мА"]

        self.__electric_box["Автомат 16А"] = sum(
            [
                int(self.__project_params["room_quantity"]) + 1,
                self.__project_params["oven"] == "Да",
                int(self.__project_params["other_electric_appliance_quantity"]),
            ]
        )
        module_counter += self.__electric_box["Автомат 16А"]

        self.__electric_box["Автомат 10А"] = (int(self.__project_params["room_quantity"]) + 1) // 2
        module_counter += self.__electric_box["Автомат 10А"]

        if self.__project_type == "частичная (комната/кухня)":
            self.__project_params["other_electric_appliance_quantity"] = "По результатам замера"
        else:
            switch_box_modules = (module_counter // 12 + 1) * 12 if module_counter < 48 else 48
            switch_box_key = f"Монтаж, сборка и подключение щита силового ({switch_box_modules}мод)"
            project_estimate[switch_box_key] = (
                f"1шт * {price[switch_box_key]} = " f"{price[switch_box_key]} руб."
            )

            # Устройство ниши под щит:
            if self.__project_params["electrical_box"] == "Встроенный":
                switch_box_key = f"Устройство ниши под щит ({switch_box_modules}мод)"
                project_estimate[switch_box_key] = (
                    f" 1шт * {price[switch_box_key]} = " f"{price[switch_box_key]}руб."
                )

        return project_estimate


if __name__ == "__main__":
    project_dict = {
        "project_name": "test_name",
        "project_address": "test_address",
        "project_square": 45,
        "project_type": "test_type"
    }

    proj_1 = Project.create_new_project(project_dict)

    project_dict_params = {
        "room_quantity": 3,
        "walls_material": "Бетон",
        "partitions_material": "Бетон",
        "ceiling_material": "Да",
        "sockets_quantity": 30,
        "switches_quantity": 5,
        "communication_sockets_quantity": 3,
        "light_point_quantity": 10,
        "electrical_box": "Встроенный",
        "power_cable": "Да",
        "washing_machine": "Да",
        "dishwasher": "Да",
        "boiler": "Да",
        "el_plate": "Да",
        "water_heater": "Да",
        "oven": "Да",
        "other_electric_appliance_quantity": 3,
    }

    proj_1.add_project_params(project_dict_params)

    print(project_dict_params.get("room_quantity"))

    print(proj_1._Project__project_params)

    print(proj_1.get_estimate_by_project_params())

    print(proj_1._Project__electric_box)




