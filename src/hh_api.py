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
        self.__vacancies = []

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

    def get_vacancies(self, selected_employers: list) -> list:
        """Метод получения данных о вакансиях работодателя с сайта hh.ru"""
        self._BaseApi__connect_api()
        for employer in selected_employers:
            response = requests.get(f"{self.__url}/vacancies?employer_id={employer['id']}")
            selected_vacancies = response.json()["items"]
            self.__vacancies.extend(selected_vacancies)
        return self.__vacancies
