import psycopg2

from src.dbmanager import DBManager
from src.hh_api import HeadHunter

hh_obj = HeadHunter()


def get_employers_from_hh() -> list:
    """Получаем список работодателей по списку их id"""
    ids = [
        9694561,
        5331842,
        53797,
        227780,
        3031009,
        23427,
        4352,
        19833,
        2180,
        1373,
    ]
    found_employers = hh_obj.get_employers(ids)
    return found_employers


def get_vacancies_from_hh() -> list:
    """Получаем список вакансий работодателей и валидируем зарплату"""
    employers_data = get_employers_from_hh()
    found_vacancies = hh_obj.get_vacancies(employers_data)
    for vac in found_vacancies:
        if vac["salary"] is None:
            vac["salary"] = 0
        elif isinstance(vac["salary"], dict):
            if not vac["salary"]["from"] is None and not vac["salary"]["to"] is None:
                vac["salary"] = int((vac["salary"]["from"] + vac["salary"]["to"]) / 2)
            elif not vac["salary"]["from"] is None and vac["salary"]["to"] is None:
                vac["salary"] = int(vac["salary"]["from"])
            else:
                vac["salary"] = int(vac["salary"]["to"])
    return found_vacancies


def create_database(database_name: str, params: dict) -> None:
    """Создание базы данных"""
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")
    conn.close()


def create_tables(database_name: str, params: dict) -> None:
    """Создаем таблицы employers и vacancies"""
    with psycopg2.connect(dbname=database_name, **params) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
            CREATE TABLE employers (
            id INT PRIMARY KEY,
            name VARCHAR(250) NOT NULL
            )
            """
            )

        with conn.cursor() as cur:
            cur.execute(
                """
            CREATE TABLE vacancies (
            id INT PRIMARY KEY,
            name VARCHAR(250) NOT NULL,
            alternate_url TEXT NOT NULL,
            salary INT NOT NULL,
            employer_id INT REFERENCES employers(id) NOT NULL
            )
            """
            )
    conn.close()


def fill_in_employers(employers_data: list, database_name: str, params: dict) -> None:
    """Заполняем таблицу employers данными о работодателях"""
    employers_ids = []
    with psycopg2.connect(dbname=database_name, **params) as conn:
        with conn.cursor() as cur:
            for employer_data in employers_data:
                if employer_data["id"] not in employers_ids:
                    cur.execute(
                        """INSERT INTO employers (id, name) VALUES (%s, %s)""",
                        (f"{employer_data["id"]}", f"{employer_data["name"]}"),
                    )
                    employers_ids.append(employer_data["id"])
                else:
                    continue
    conn.close()


def fill_in_vacancies(vacancies_data: list, database_name: str, params: dict) -> None:
    """Заполняем таблицу vacancies данными о вакансиях"""
    vacancies_ids = []
    with psycopg2.connect(dbname=database_name, **params) as conn:
        with conn.cursor() as cur:
            for vacancy_data in vacancies_data:
                if vacancy_data["id"] not in vacancies_ids:
                    cur.execute(
                        """
                    INSERT INTO vacancies (id, name, alternate_url, salary, employer_id)
                    VALUES (%s, %s, %s, %s, %s)""",
                        (
                            f"{vacancy_data["id"]}",
                            f"{vacancy_data["name"]}",
                            f"{vacancy_data["alternate_url"]}",
                            f"{vacancy_data["salary"]}",
                            f"{vacancy_data['employer']['id']}",
                        ),
                    )
                    vacancies_ids.append(vacancy_data["id"])
                else:
                    continue

    conn.close()


def get_keyword() -> str:
    """Получаем ключевое слово от пользователя для фильтрации вакансий"""
    user_word = input("Введите слово для поиска вакансий: ")
    return user_word


def user_interaction(database_name: str, params: dict) -> None:
    """Получаем от пользователя данные для вывода необходимой ему информации"""
    hhdb = DBManager()
    user_input = input(
        "Укажите пункт, информацию по которому Вам бы хотелось получить:\n"
        "1. Список всех компаний и количество вакансий у каждой компании.\n"
        "2. Список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.\n"
        "3. Среднюю зарплату по вакансиям.\n"
        "4. Список всех вакансий, у которых зарплата выше средней по всем вакансиям.\n"
        "5. Список всех вакансий, в названии которых содержатся переданные в метод слова.\n"
    )
    if user_input == "1":
        hhdb.get_companies_and_vacancies_count(database_name, params)
    elif user_input == "2":
        hhdb.get_all_vacancies(database_name, params)
    elif user_input == "3":
        hhdb.get_avg_salary(database_name, params)
    elif user_input == "4":
        hhdb.get_vacancies_with_higher_salary(database_name, params)
    elif user_input == "5":
        keyword = get_keyword()
        hhdb.get_vacancies_with_keyword(database_name, params, keyword)
    else:
        print("Такого пункта не существует. Попробуйте еще раз.")
