from src.utils import create_database, create_table, insert_tables
from src.db_manager import DBManager


name_db = "test1_course"
create_database(name_db)
create_table(name_db)
insert_tables(name_db)

db_manager = DBManager(name_db)

while True:
    print("Какую информацию вы хотите получить?")
    print("1. Список всех компаний")
    print("2. Список всех вакансий с указанием названия компании")
    print("3. Средняя зарплата по вакансиям")
    print("4. Список вакансий, зарплата которых выше средней по всем вакансиям")
    print("5. Получить список всех вакансий, в названии которых содержится слово из вашего запроса")
    answer = input()


# # print(db_manager.get_all_employers())
# print(db_manager.get_companies_and_vacancies_count())
# print(db_manager.get_all_vacancies())
# print(db_manager.get_avg_salary())
# print(db_manager.get_vacancies_with_higher_salary())
# print(db_manager.get_vacancies_with_keyword('Кладовщик'))