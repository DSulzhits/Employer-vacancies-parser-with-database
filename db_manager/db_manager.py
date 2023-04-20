from fill_DB.fill_database import ConnectDB


class DBManager:
    # @staticmethod
    # def get_info_employers():
    #     conn = ConnectDB.connect_to_db()
    #     try:
    #         with conn:
    #             with conn.cursor() as cur:
    #                 cur.execute("SELECT * FROM employers")
    #                 companies = cur.fetchall()
    #     finally:
    #         conn.close()
    #     return companies

    # @staticmethod
    # def get_info_vacancies():
    #     conn = ConnectDB.connect_to_db()
    #     try:
    #         with conn:
    #             with conn.cursor() as cur:
    #                 cur.execute("SELECT * FROM vacancies")
    #                 vacancies_info = cur.fetchall()
    #     finally:
    #         conn.close()
    #     return vacancies_info

    @classmethod
    def get_companies_and_vacancies_count(cls):
        conn = ConnectDB.connect_to_db()
        employers_vac_list = []
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT employer_name, COUNT(vacancies) AS vacancy_count 
                                   FROM employers 
                                   INNER JOIN vacancies 
                                   USING(employer_id) 
                                   GROUP BY employer_name 
                                   ORDER BY vacancy_count DESC""")
                    emp_vac_all = cur.fetchall()
                    for emp_vac in emp_vac_all:
                        emp, vac_count = emp_vac
                        employers_vac_list.append(f"Работодатель {emp}: число вакансий {vac_count}")
        finally:
            conn.close()
        return employers_vac_list

    @classmethod
    def get_avg_salary(cls):
        conn = ConnectDB.connect_to_db()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT ROUND(AVG(vacancy_salary_from)) FROM vacancies")
                    avg_salary = cur.fetchone()[0]
        finally:
            conn.close()
        return f"Средняя заработная плата от {avg_salary} рублей"

    @classmethod
    def get_vacancies_with_higher_salary(cls):
        salaries_top_list = []
        conn = ConnectDB.connect_to_db()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT vacancy_name, vacancy_salary_from
                                   FROM vacancies
                                   WHERE vacancy_salary_from > (SELECT AVG(vacancy_salary_from) FROM vacancies) 
                                   ORDER BY vacancy_salary_from DESC""")
                    salaries_top = cur.fetchall()
                    for salary_top in salaries_top:
                        name, sal_top = salary_top
                        salaries_top_list.append(f"Вакансия: {name}, заработная плата: {sal_top}")
        finally:
            conn.close()
        return salaries_top_list

    @classmethod
    def get_vacancies_with_keyword(cls, keyword):
        vacancies_list = []
        conn = ConnectDB.connect_to_db()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        f"""SELECT vacancy_name, vacancy_url, vacancy_salary_from, vacancy_salary_to FROM vacancies
                            WHERE vacancy_name LIKE '%{keyword}%'""")
                    vacancies_keyword = cur.fetchall()
                    for vacancy in vacancies_keyword:
                        name, url, sal_from, sal_to = vacancy
                        if sal_from is None:
                            sal_from = 'не указано'
                        if sal_to is None:
                            sal_to = 'не указано'
                        vacancies_list.append(f"Вакансия: {name}, url: {url}, зарплата от: {sal_from}, до: {sal_to}")
        finally:
            conn.close()
        return vacancies_list


db = DBManager
data = db.get_companies_and_vacancies_count()
# for d in data:
#     print(d)
salary = db.get_avg_salary()
print(salary)
vacancies = db.get_vacancies_with_keyword("Python")
# for vac in vacancies:
#     print(vac)
top_salary = db.get_vacancies_with_higher_salary()
# for top in top_salary:
#     print(top)
