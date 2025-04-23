import requests

from src.base_api import BaseApi


class HeadHunter(BaseApi):
    """Создаем на основе базового класса BaseApi класс для работы с HH"""

    __url: str
    __params: dict
    __employers: list

    def __init__(self) -> None:
        """Метод инициализации экземпляра класса"""
        self.__url = "https://api.hh.ru"
        self.__params = {"page": 0, "per_page": 100}
        self.__employers = []

    def _BaseApi__connect_api(self) -> None:
        """Метод для проверки подключения к API"""
        response = requests.get(self.__url, params=self.__params)
        if response.status_code != 200:
            raise requests.exceptions.RequestException

    def get_employers(self, employer_ids: list[int]) -> list:
        """Метод получения данных о работодателях с сайта hh.ru"""
        try:
            self._BaseApi__connect_api()
            while self.__params.get("page") != 20:
                for employer_id in employer_ids:
                    response = requests.get(f"{self.__url}/employers/{employer_id}")
                    employer_data = response.json()
                    self.__employers.append(employer_data)
                    self.__params["page"] += 1
        except requests.exceptions.RequestException as e:
            print(f"Не удалось получить данные. Возникла ошибка: {e}")
            return []
        else:
            return self.__employers

    def get_vacancies(self, employer_id: int) -> list:
        """Метод получения данных о вакансиях работодателя с сайта hh.ru"""
        vacancies = []
        self._BaseApi__connect_api()
        response = requests.get(f"{self.__url}/vacancies?employer_id={employer_id}")
        selected_vacancies = response.json()["items"]
        vacancies.extend(selected_vacancies)
        return vacancies


# Пример использования:
# ids = [
#     9694561,
#     3529,
#     53797,
#     227780,
#     3809,
#     78638,
#     907345,
#     84585,
#     2180,
#     3127,
# ]
# hh_obj = HeadHunter()
# found_employers = hh_obj.get_employers(ids)
#
# for employer in found_employers:
#     print(employer['id'], employer['name'])
#
#     vacancies_of_employer = hh_obj.get_vacancies(employer["id"])
#
#     for vacancy in vacancies_of_employer:
#         print(vacancy['id'], vacancy['name'], vacancy['alternate_url'], vacancy['salary'], vacancy['employer'])
