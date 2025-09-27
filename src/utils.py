import psycopg2
from src.config import config
from src.hh_api import HHParser


def create_database(name_db):
    params = config()
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {name_db}")
    cur.execute(f"CREATE DATABASE {name_db}")

    cur.close()
    conn.close()


def create_table(name_db):
    params = config()
    conn = psycopg2.connect(dbname=name_db, **params)
    with conn:
        with conn.cursor()as cur:
            cur.execute(
                """
                CREATE TABLE employers (
                id int PRIMARY KEY,
                name varchar(255) NOT NULL
                        )
                    """)

            cur.execute("""
                            CREATE TABLE vacancies (
                                id INTEGER PRIMARY KEY,
                                employer_id INTEGER REFERENCES employers(id),
                                name VARCHAR(255) NOT NULL,
                                salary_from INTEGER,
                                salary_to INTEGER,
                                url VARCHAR(255)
                            )
                        """)
    conn.close()


def insert_tables(name_db):
    hh_parser = HHParser()
    employers = hh_parser.get_employers()
    params = config()
    conn = psycopg2.connect(dbname=name_db, **params)
    with conn:
        with conn.cursor() as cur:
            for employer in employers:
                cur.execute("INSERT INTO employers VALUES (%s, %s)", (employer["id"], employer["name"]))
                # скрипт на добавление вакансий

    conn.close()
