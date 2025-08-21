"""
In this module we have different classes for project which include
- Project :
    - name(user_name or address)
    - project type
"""


class PowerLine:
    def __init__(self):
        pass


class UserProjects:
    """
    Class UserProjects with main parameters of project
    """

    project_name: str
    project_type: str
    project_power_lines_list: list[PowerLine]


    def __init__(self, project_name, project_type):
        self.project_name = project_name
        self.project_type = project_type




