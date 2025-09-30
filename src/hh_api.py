from typing import Any, Dict, List

import requests


class HHParser:
    def __init__(self) -> None:
        """Инициализирует парсер с базами URL API HH"""
        self.__url_employer = "https://api.hh.ru/employers"
        self.__url_vacancies = "https://api.hh.ru/vacancies"

    def get_employers(self) -> List[Dict[str, Any]]:
        """Получает список работодателей с открытыми вакансиями."""
        params: Dict[str, Any] = {"sort_by": "by_vacancies_open", "per_page": 10}
        response: requests.Response = requests.get(self.__url_employer, params=params)
        response.raise_for_status()
        employers = response.json()["items"]
        return [
            {"id": employer["id"], "name": employer["name"]} for employer in employers
        ]

    def get_vacancies_by_employer(self, employer_id) -> List[Dict[str, Any]]:
        """Получает список вакансий для указанного работодателя"""
        params = {"employer_id": employer_id, "per_page": 100}
        response = requests.get(self.__url_vacancies, params=params).json()["items"]
        return response

    def get_all_vacancies_by_employers(self) -> List[Dict[str, Any]]:
        """Получаем все вакансии для всех работодателей"""
        employers = self.get_employers()
        all_vacancies = []
        for employer in employers:
            vacancies = self.get_vacancies_by_employer(employer["id"])
            all_vacancies.extend(
                [self.filter_vacancy(vacancy) for vacancy in vacancies]
            )
        return all_vacancies

    @staticmethod
    def filter_vacancy(vacancy: Dict[str, Any]) -> Dict[str, Any]:
        """Фильтрует и нормализует данные вакансии, извлекая ключевые поля."""
        if vacancy["salary"]:
            salary_from = vacancy["salary"]["from"] if vacancy["salary"]["from"] else 0
            salary_to = vacancy["salary"]["to"] if vacancy["salary"]["to"] else 0
        else:
            salary_from = 0
            salary_to = 0
        return {
            "id": vacancy["id"],
            "name_vacancy": vacancy["name"],
            "area": vacancy["area"]["name"],
            "url": vacancy["alternate_url"],
            "salary_from": salary_from,
            "salary_to": salary_to,
        }
