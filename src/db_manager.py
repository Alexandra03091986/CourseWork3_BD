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

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
         названия вакансии и зарплаты и ссылки на вакансию."""
        return self.execute_query(
            """
            SELECT name as company_name, name_vacancy, salary_from, salary_to, url_vacancy FROM employers 
            INNER JOIN vacancies ON employers.id = vacancies.employer_id 
            ORDER BY company_name, name_vacancy
            """
        )

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        return self.execute_query(
            """
            SELECT name_vacancy, 
            ROUND(AVG( 
            CASE 
            WHEN salary_from > 0 and salary_to > 0 THEN (salary_from + salary_to) / 2 
            WHEN salary_from > 0 THEN salary_from
            WHEN salary_to > 0 THEN salary_to 
            ELSE NULL 
            END), 2) as avg_salary 
            from vacancies 
            WHERE (salary_from is not null and salary_from > 0) 
            OR (salary_to is not null and salary_to > 0) 
            GROUP BY name_vacancy 
            ORDER BY name_vacancy;
            """
        )

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        return self.execute_query(
            """
            WITH all_salaries AS (
            SELECT name_vacancy,  
            CASE 
            WHEN salary_from > 0 and salary_to > 0 THEN (salary_from + salary_to) / 2 
            WHEN salary_from > 0 THEN salary_from 
            WHEN salary_to > 0 THEN salary_to 
            ELSE NULL 
            END as salary 
            FROM vacancies 
            WHERE (salary_from is not null and salary_from > 0) 
            OR (salary_to is not null and salary_to > 0)
            ) 
            SELECT name_vacancy, salary 
            FROM all_salaries 
            WHERE salary > (SELECT AVG(salary) FROM all_salaries) 
            ORDER BY salary DESC
            """
        )
