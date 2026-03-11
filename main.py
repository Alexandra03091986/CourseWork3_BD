from typing import NoReturn

from src.db_manager import DBManager
from src.utils import create_database, create_table, insert_tables


def main() -> None:
    """Главная функция приложения для работы с базой данных вакансий"""
    print("Подождите идет сбор данных ...")

    name_db = "test1_course"
    create_database(name_db)
    print("Подождите ещё чуть-чуть...")
    create_table(name_db)
    print("Осталось совсем не много...")
    insert_tables(name_db)

    db_manager = DBManager(name_db)

    while True:
        print("\n Какую информацию вы хотите получить?")
        print("1. Список всех компаний")
        print("2. Список всех вакансий с указанием названия компании")
        print("3. Средняя зарплата по вакансиям")
        print("4. Список вакансий, зарплата которых выше средней по всем вакансиям")
        print(
            "5. Получить список всех вакансий, в названии которых содержится слово из вашего запроса"
        )
        print("6. Выход")
        answer = input()
        print("Подождите идет обработка запроса...")

        if answer == "1":
            for elem in db_manager.get_companies_and_vacancies_count():
                print(
                    f"Название компании: {elem[0]}\n "
                    f"Количество вакансий: {elem[1]}\n"
                )
        elif answer == "2":
            for elem in db_manager.get_all_vacancies():
                print(
                    f"Название компании: {elem[0]}\n"
                    f"Название вакансии: {elem[1]}\n"
                    f"Зарплата от {elem[2]} руб. до {elem[3]} руб.\n"
                    f"Ссылка на вакансию: {elem[4]}\n"
                )
        elif answer == "3":
            for elem in db_manager.get_avg_salary():
                print(
                    f"Название вакансии: {elem[0]}\n"
                    f"Средняя зарплата {elem[1]} руб.\n"
                )
        elif answer == "4":
            for elem in db_manager.get_vacancies_with_higher_salary():
                print(
                    f"Название вакансии: {elem[0]}\n"
                    f"Средняя зарплата {elem[1]} руб.\n"
                )
        elif answer == "5":
            query_word = input("Введите название вакансии: ")

            for elem in db_manager.get_vacancies_with_keyword(query_word):

                print(
                    f"Название вакансии: {elem[0]}\n"
                    f"Зарплата от {elem[1]} руб. до {elem[2]} руб.\n"
                    f"Ссылка на вакансию: {elem[3]}\n"
                )
            print(
                f"Найдено вакансий - {len(db_manager.get_vacancies_with_keyword(query_word))}"
            )
        elif answer == "6":
            break


if __name__ == "__main__":
    main()
