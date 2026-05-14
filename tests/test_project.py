from src.project import Project

def test_project_create_new_project(test_project_dict: dict) -> None:

    test_project = Project.create_new_project(test_project_dict)

    assert test_project._Project__project_name == test_project_dict["project_name"]


def test_project_add_project_params(test_project_dict: dict, test_project_params_dict: dict) -> None:

    test_project = Project.create_new_project(test_project_dict)
    test_project.add_project_params(test_project_params_dict)

    print(test_project._Project__project_name)

    assert  test_project._Project__project_params == {
        'room_quantity': 3, 'walls_material': 'Бетон', 'partitions_material': 'Бетон', 'ceiling_material': 'Да',
         'sockets_quantity': 30, 'switches_quantity': 5, 'communication_sockets_quantity': 3,
         'light_point_quantity': 10, 'electrical_box': 'Встроенный', 'power_cable': 'Да', 'washing_machine': 'Да',
         'dishwasher': 'Да', 'boiler': 'Да', 'el_plate': 'Да', 'water_heater': 'Да', 'oven': 'Да',
         'other_electric_appliance_quantity': 3
    }

    assert  test_project.get_estimate_by_project_params() == {
         'Название проекта': 'test_name', 'Адрес объекта': 'test_address', 'Список работ': 'До замера',
         'Объект:': 'test_type, 45м2', 'Устройство отверстия под подрозетник (бетон)': '38шт * 300 = 11400руб.',
         'Штробление стен 20*20 (бетон)': '96м.п. * 300 = 28800руб',
         'Протяжка кабеля силового 3*6.0 / 5*2.5': '36м.п. * 120 = 4320руб',
         'Протяжка кабеля силового 3*2.5': '190.0м.п. * 100 = 19000.0руб',
         'Протяжка кабеля силового 3*1.5': '100.0м.п. * 100 = 10000.0руб',
         'Монтаж подрозетника': '38шт * 150 = 5700руб.', 'Замена вводного кабеля': ' 1шт * 5000 = 5000руб.',
         'Монтаж, сборка и подключение щита силового (24мод)': '1шт * 12000 = 12000 руб.',
         'Устройство ниши под щит (24мод)': ' 1шт * 6000 = 6000руб.'
    }
