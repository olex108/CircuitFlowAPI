from src.calculations import parameters, option_functions
from fastapi import FastAPI
from src.config.settings import get_settings
from contextlib import asynccontextmanager
from src.config.database import dispose_session
from src.routers import key, design, estimate
from src.config.broker_taskiq import broker


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    if not broker.is_worker_process:
        await broker.sturtup()
    yield
    # shutdown
    # Отключение БД
    await dispose_session()
    await broker.shutdown()


main_app = FastAPI(
    lifespan=lifespan
)


main_app.include_router(key.router)
main_app.include_router(design.router)
main_app.include_router(estimate.router)


# def select_option():
#     """
#     Функция выбора действия пользователя запускается при вызове программы и предлагает
#     пользователю варианты действий:
#     - Создать новый проект
#     - Открыть существующий проект
#     """
#
#     operation = input(f"Выберите действие:\nСоздать новый проект\nОткрыть существующий проект\nРасценки\n")
#
#     if operation == "Создать новый проект":
#         option_functions.create_new_project()
#     elif operation == "Открыть существующий проект":
#         option_functions.verification_name_password()
#     elif operation == "Расценки":
#         option_functions.print_dictionary_lines(parameters.price_list)
#
#     select_option()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()

    uvicorn.run(
        "src.main:main_app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
