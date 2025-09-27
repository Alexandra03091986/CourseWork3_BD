import psycopg2

from src.config import config


class DBManager:
    """Класс для управления подключением к базе данных и выполнением SQ-запросов.
    """
    def __init__(self, db_name):
        """Инициализирует менеджер базы данных с указанным именем БД"""
        self.__db_name = db_name

    def execute_query(self, query):
        """Выполняет SQ-запрос к базе данных и возвращает результаты."""
        params = config()
        conn = psycopg2.connect(dbname=self.__db_name, **params)
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                res = cur.fetchall()
        conn.close()
        return  res


    def get_all_employers(self):
        return self.execute_query("SELECT * FROM employers")

    def get_companies_and_vacancies_count(self):
        """ Получает список всех компаний и количество вакансий у каждой компании."""
        return self.execute_query("""
            SELECT DISTINCT name, COUNT(*) FROM employers 
            INNER JOIN vacancies ON employers.id = vacancies.employer_id 
            GROUP BY name
        """)

# get_companies_and_vacancies_count()- получает список всех компаний и количество вакансий у каждой компании.
#
# важно: использовать JOIN чтобы одним запросом получить работодателя и все его вакансии