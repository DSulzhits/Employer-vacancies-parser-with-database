from fill_DB.fill_database import ConnectDB


class DBManager:
    @staticmethod
    def get_info_employers():
        conn = ConnectDB.connect_to_db()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM employers")
                    companies = cur.fetchall()
        finally:
            conn.close()
        return companies

    @staticmethod
    def get_info_vacancies():
        conn = ConnectDB.connect_to_db()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM vacancies")
                    vacancies = cur.fetchall()
        finally:
            conn.close()
        return vacancies

    @classmethod
    def get_companies_and_vacancies_count(cls):
        employers_list = []
        for company in cls.get_info_employers():
            vacancies_list = []
            emp_id, name, url = company
            for vacancy in cls.get_info_vacancies():
                vac_id, vac_name, vac_url, vac_from, vac_to, vac_emp_id = vacancy
                if vac_emp_id == emp_id:
                    vacancies_list.append(vac_name)
            vacancies_count = {f'{name}': len(vacancies_list)}
            employers_list.append(vacancies_count)
        return employers_list


# Работодатель Skyeng id 1122462 уже существует
# Работодатель Skillbox id 2863076 уже существует
# Работодатель Лаборатория Касперского id 1057 уже существует
# Работодатель Lesta Games id 856498 уже существует
# Работодатель VK id 15478 уже существует
# Работодатель LG Electronics Inc. id 102501 уже существует
# Работодатель SberTech id 906557 уже существует
# Работодатель YADRO id 1993194 уже существует
# Работодатель Доктор Веб id 8884 уже существует
# Работодатель GeekBrains id 1111672 уже существует
# Вакансия Data Analyst id 79476191 уже существует


db = DBManager
data = db.get_companies_and_vacancies_count()
print(data)
