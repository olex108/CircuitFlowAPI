from src.electric_point import OutletPoint, LightingPoint, SwitchPoint


class ElectricLine:
    """
    Class describe electric lines
    """

    line_num: int
    line_name: str
    line_power: int


    def __init__(self, line_num: int, line_name: str, line_power: int) -> None:

        self.line_num = line_num
        self.line_name = line_name
        self.line_power = line_power


class ElectricOutletLine(ElectricLine):
    """
    Class describe electric lines of outlet
    """

    outlet_points_list : list[OutletPoint]

    def __init__(self, line_num: int, line_name: str, line_power: int) -> None:
        """
        Initialisation of electric line
        """

        super().__init__(line_num, line_name, line_power)
        self.outlet_points_list = []

    def add_outlet_point(self, new_point: OutletPoint):
        """Add new point"""

        self.outlet_points_list.append(new_point)

    def get_electric_line_params(self):
        """
        Method to get params of electric line:
        quantity of cable,
        quantity of sockets,
        """

        pass


class ElectricLightLine(ElectricLine):
    """
    Class describe electric lines of outlet
    """

    switch_light_dict : dict[SwitchPoint, LightingPoint]

    def __init__(self, line_num: int, line_name: str, line_power: int) -> None:
        """
        Initialisation of electric line
        """

        super().__init__(line_num, line_name, line_power)
        self.switch_light_dict = {}

    def add_switch_light_pair(self, new_pair: OutletPoint):
        """Add new point"""

        pass
        # self.switch_light_dict.append(new_pair)

    def get_electric_line_params(self):
        """
        Method to get params of electric line:
        quantity of cable,
        quantity of sockets,
        """

        pass

class ElectricApplianceLine(ElectricLine):
    """

    """

class ElectricPowerLine(ElectricLine):
    """

    """

