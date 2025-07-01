"""
Главная страница проекта позволяет выбирать основные функции программы:
- "Открыть существующий проект" вызывает функцию - create_new_project()
- "Открыть существующий проект" вызывает функцию верификации пользователя - verification_name_password()
- "Расценки": вызывает функцию вывода данных словаря в который передает данные словаря расценок
print_dictionary_lines(parameters.price_list)

Функция select_option вызывает саму себя для создания рекурсии
"""


from src import option_functions

from src import parameters


def select_option():
    """
    Функция выбора действия пользователя запускается при вызове программы и предлагает
    пользователю варианты действий:
    - Создать новый проект
    - Открыть существующий проект
    - Расценки
    """

    operation = input(f"Выберите действие:\nСоздать новый проект\nОткрыть существующий проект\nРасценки\n")

    if operation == "Создать новый проект":
        option_functions.create_new_project()
    elif operation == "Открыть существующий проект":
        option_functions.verification_name_password()
    elif operation == "Расценки":
        option_functions.print_dictionary_lines(parameters.price_list)

    select_option()

