from src.electric_line import ElectricLine, ElectricOutletLine, ElectricLightLine, ElectricApplianceLine


def test_electric_outlet_line_initialisation() -> None:
    test_line = ElectricOutletLine("test_name", 16)
    test_2 = ElectricOutletLine("test2", 16)

    assert test_line.line_num == 1
    assert test_2.line_num == 2