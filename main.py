from config import config
from src.utils import create_database, fill_in_employers, create_tables, get_employers_from_hh, get_vacancies_from_hh, \
    fill_in_vacancies, user_interaction


def main() -> None:
    """Основная функция, объединяющая функционал"""
    params = config()

    employers_to_fill_in_tables = get_employers_from_hh()
    vacancies_to_fill_in_tables = get_vacancies_from_hh()

    create_database("hhdatabase", params)
    create_tables("hhdatabase", params)

    fill_in_employers(employers_to_fill_in_tables,"hhdatabase", params)
    fill_in_vacancies(vacancies_to_fill_in_tables,"hhdatabase", params)

    user_interaction("hhdatabase", params)


if __name__ == '__main__':
    main()
