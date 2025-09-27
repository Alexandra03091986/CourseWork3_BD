import psycopg2
from src.config import config
from src.hh_api import HHParser


def create_database(name_db):
    """ Создание новой базы данных PostgreSQL.
    Функция подключается к серверу PostgreSQL,
    удаляет базу данных если она существует и
    создает новую пустую базу данных с указанным именем."""
    params = config()
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {name_db}")
    cur.execute(f"CREATE DATABASE {name_db}")

    cur.close()
    conn.close()


def create_table(name_db):
    """Создание таблиц в указанной БД для хранения данных.
     Функция создает две связанные таблицы:
     employers - таблица работодателей
     vacancies - таблица вакансий с внешним ключом employers
     """
    params = config()
    conn = psycopg2.connect(dbname=name_db, **params)
    with conn:
        with conn.cursor()as cur:
            cur.execute(
                """
                CREATE TABLE employers (
                id INTEGER PRIMARY KEY,
                name varchar(255) NOT NULL
                )
                """
            )

            cur.execute("""
                            CREATE TABLE vacancies (
                            id INTEGER PRIMARY KEY,
                            employer_id INTEGER REFERENCES employers(id),
                            name_vacancy VARCHAR(255) NOT NULL,
                            salary_from INTEGER,
                            salary_to INTEGER,
                            url_vacancy VARCHAR(255)
                            )
                        """)
    conn.close()


def insert_tables(name_db):
    """Заполняет таблицы БД данными о работодателях и их вакансиях из API HH."""
    hh_parser = HHParser()
    employers = hh_parser.get_employers()
    params = config()
    conn = psycopg2.connect(dbname=name_db, **params)
    with conn:
        with conn.cursor() as cur:
            for employer in employers:
                cur.execute(
                    "INSERT INTO employers VALUES (%s, %s)",
                    (employer["id"], employer["name"])
                )

                vacancies = hh_parser.get_vacancies_by_employer(employer["id"])
                for vacancy in vacancies:
                    filter_vacancy = HHParser.filter_vacancy(vacancy)
                    cur.execute(
                        "INSERT INTO vacancies ("
                        "id,"
                        " employer_id,"
                        " name_vacancy,"
                        " salary_from, "
                        "salary_to,"
                        " url_vacancy"
                        ") VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING",
                        (filter_vacancy["id"], employer["id"], filter_vacancy["name_vacancy"],
                         filter_vacancy["salary_from"],
                         filter_vacancy["salary_to"],
                         filter_vacancy["url"])
                    )

    conn.close()
