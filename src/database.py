import psycopg2


class PostgresDatabase:
    def __init__(self, user: str, password: str, host: str = 'localhost', port: str = '5432'):
        self.__create_database(user, password, host, port)

        self.conn = psycopg2.connect(dbname="electric_project", user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()

        # self.__create_tables()

    def __create_database(self, user: str, password: str, host: str = 'localhost', port: str = '5432'):
        """Создание базы данных"""

        try:
            conn = psycopg2.connect(user=user, password=password, host=host, port=port)
            conn.autocommit = True
            cur = conn.cursor()

            cur.execute(f"CREATE DATABASE companies_vacations")

            cur.close()

            conn.close()

        except psycopg2.errors.DuplicateDatabase:
            pass

    # def __create_tables(self):
    #     """Создание базы данных и таблиц для сохранения данных о каналах и видео."""
    #
    #     try:
    #         with self.conn:
    #             self.cur.execute("""
    #                     CREATE TABLE companies (
    #                         company_id SERIAL PRIMARY KEY,
    #                         company_name VARCHAR(255) NOT NULL,
    #                         hh_id INTEGER NOT NULL,
    #                         url VARCHAR(255),
    #                         description TEXT
    #                     )
    #                 """)
    #
    #         with self.conn:
    #             self.cur.execute("""
    #                     CREATE TABLE vacancies (
    #                         vacancy_id SERIAL PRIMARY KEY,
    #                         company_id INT REFERENCES companies(company_id),
    #                         name VARCHAR(255) NOT NULL,
    #                         url VARCHAR(255) NOT NULL,
    #                         salary_from INTEGER,
    #                         salary_to INTEGER,
    #                         description TEXT
    #                     )
    #                 """)
    #
    #         self.conn.commit()
    #
    #     except psycopg2.errors.DuplicateTable:
    #         pass


# if __name__ == '__main__':
#     params = config()
#     db = PostgresDatabase(**params)