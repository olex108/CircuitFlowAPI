from src.calculations import parameters, option_functions
from fastapi import FastAPI
from src.config.settings import get_settings
from contextlib import asynccontextmanager
from src.config.database import dispose_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    # Отключение БД
    await dispose_session()


main_app = FastAPI(
    lifespan=lifespan
)


def select_option():
    """
    Функция выбора действия пользователя запускается при вызове программы и предлагает
    пользователю варианты действий:
    - Создать новый проект
    - Открыть существующий проект
    """

    operation = input(f"Выберите действие:\nСоздать новый проект\nОткрыть существующий проект\nРасценки\n")

    if operation == "Создать новый проект":
        option_functions.create_new_project()
    elif operation == "Открыть существующий проект":
        option_functions.verification_name_password()
    elif operation == "Расценки":
        option_functions.print_dictionary_lines(parameters.price_list)

    select_option()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()

    uvicorn.run(
        "src.main:main_app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )

