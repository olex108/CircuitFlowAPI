import json
import os
from abc import ABC, abstractmethod
from typing import Any
from pathlib import Path
from config import PATH



class FileHandler(ABC):
    """
    Abstract class for work with files, include save, get or del vacations from files
    """

    @abstractmethod
    def save_data(self, save_data) -> None:
        pass

    @abstractmethod
    def get_data(self) -> list:
        pass

    # @abstractmethod
    # def del_data(self) -> None:
    #     pass


class CSVHandler(FileHandler):
    """
    Class for work with CSV files, include save, get or del vacations.
    """

    file_name: str

    def __init__(self, path_to_file: Path) -> None:
        self.__path_to_file = path_to_file

    def save_vacancies(self, save_data) -> None:

        pass

    @abstractmethod
    def get_vacancies(self) -> list:

        pass

    def del_vacancies(self, *args: list[int]) -> None:

        pass


class JSONHandler(FileHandler):
    """
    Class for work with JSON files, with include save, get or del data.
    """

    path_to_file: Path

    def __init__(self, path_to_file: Path) -> None:
        self.__path_to_file = path_to_file


    def save_data(self, save_data: Any) -> None:
        """
        Method to save data in JSON file.

        :param save_data: data
        """

        with open(self.__path_to_file, "w", encoding="utf-8") as file:
            json.dump(save_data, file, ensure_ascii=False, indent=4)


    def get_data(self) -> Any:
        """
        Method to get data from JSON file

        :return data_json: data
        """

        try:
            with open(self.__path_to_file, "r", encoding="utf-8") as file:
                data_json = json.load(file)
            return data_json
        except FileNotFoundError:
            print("Файл не найден")
            return None

    def del_vacancies(self, list_of_index: list[int]) -> None:
        """
        Method to del vacancies from JSON file by indexes

        :param list_of_index: list of indexes for del from file
        """

        pass
        # try:
        #     with open(self.__path_to_file, "r", encoding="utf-8") as file:
        #         file_data = json.load(file)
        #
        #     for index in list_of_index:
        #         del file_data[index]
        #
        #     with open(self.__path_to_file, "w", encoding="utf-8") as file:
        #         json.dump(file_data, file, ensure_ascii=False, indent=4)
        #
        # except IndexError:
        #     print("Индекс выходит за рамки списка")
        #
        # except FileNotFoundError:
        #     print("Файл не найден")
