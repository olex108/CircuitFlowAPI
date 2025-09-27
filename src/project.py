from src.electric_line import ElectricLine

class Project(object):
    """Class of project"""

    project_name: str
    project_address: str
    project_square: int
    project_type: str
    electric_lines_list: list[ElectricLine]
    project_input_params: dict
    project_estimate_params: dict


    def __init__(self, project_name, project_address, project_square, project_type):
        """"""

        self.project_name = project_name
        self.project_address = project_address
        self.project_square = project_square
        self.project_type = project_type
        self.electric_lines_list = []
        self.project_input_params = {}
        self.project_estimate_params = {}






