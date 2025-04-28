import psycopg2


class DBManager:
    """Создаем класс для работы с базой данных"""

    def get_companies_and_vacancies_count(self, database_name: str, params: dict) -> None:
        """Получаем список всех компаний и количество вакансий у каждой компании"""
        with psycopg2.connect(dbname=database_name, **params) as self.conn:
            with self.conn.cursor() as self.cur:
                self.cur.execute(
                    """
                SELECT e.name, COUNT (v.id) as cnt
                FROM employers e
                JOIN vacancies v
                ON e.id = v.employer_id
                GROUP BY e.name
                ORDER BY cnt DESC"""
                )
                result = self.cur.fetchall()
        for row in result:
            print(row)
        self.conn.close()

    def get_all_vacancies(self, database_name: str, params: dict) -> None:
        """Получаем список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию"""
        with psycopg2.connect(dbname=database_name, **params) as self.conn:
            with self.conn.cursor() as self.cur:
                self.cur.execute(
                    """
                SELECT e.name, v.name, v. salary, v.alternate_url
                FROM employers e
                JOIN vacancies v
                ON e.id = v.employer_id                
                """
                )
                result = self.cur.fetchall()
        for row in result:
            print(row)
        self.conn.close()

    def get_avg_salary(self, database_name: str, params: dict) -> None:
        """Получаем среднюю зарплату по вакансиям"""
        with psycopg2.connect(dbname=database_name, **params) as self.conn:
            with self.conn.cursor() as self.cur:
                self.cur.execute(
                    """
                    SELECT round(avg(salary), 2) as avg_salary
                    FROM vacancies
                    WHERE salary <> 0
                    """
                )
                result = self.cur.fetchall()
        for row in result:
            print(row)
        self.conn.close()

    def get_vacancies_with_higher_salary(self, database_name: str, params: dict) -> None:
        """Получаем список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        with psycopg2.connect(dbname=database_name, **params) as self.conn:
            with self.conn.cursor() as self.cur:
                self.cur.execute(
                    """
                    SELECT * 
                    FROM vacancies
                    WHERE salary > (SELECT round(avg(salary), 2) as avg_salary FROM vacancies WHERE salary <> 0)
                    """
                )
                result = self.cur.fetchall()
        for row in result:
            print(row)
        self.conn.close()

    def get_vacancies_with_keyword(self, database_name: str, params: dict, keyword: str) -> None:
        """Получаем список всех вакансий, в названии которых содержится переданное в метод слово"""
        with psycopg2.connect(dbname=database_name, **params) as self.conn:
            with self.conn.cursor() as self.cur:
                self.cur.execute("SELECT * FROM vacancies WHERE name ILIKE %s", ("%" + keyword + "%",))

                result = self.cur.fetchall()
        for row in result:
            print(row)
        self.conn.close()
