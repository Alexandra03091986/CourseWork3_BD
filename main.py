from src.utils import create_database, create_table, insert_tables
from src.db_manager import DBManager


name_db = "test1_course"
create_database(name_db)
create_table(name_db)
insert_tables(name_db)

db_manager = DBManager(name_db)
# # print(db_manager.get_all_employers())
# print(db_manager.get_companies_and_vacancies_count())
# print(db_manager.get_all_vacancies())
# print(db_manager.get_avg_salary())
print(db_manager.get_vacancies_with_higher_salary())
