import pytest

from src.project import Project

@pytest.fixture()
def test_project_dict() -> dict:
    return {
        "project_name": "test_name",
        "project_address": "test_address",
        "project_square": 45,
        "project_type": "test_type"
    }


@pytest.fixture()
def test_project_params_dict() -> dict:
    return {
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