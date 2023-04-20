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
        conn = ConnectDB.connect_to_db()
        employers_vac_list = []
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """SELECT employer_name, COUNT(vacancies) AS vacancy_count 
                        FROM employers 
                        INNER JOIN vacancies 
                        USING(employer_id) 
                        GROUP BY employer_name 
                        ORDER BY vacancy_count DESC""")
                    emp_vac_all = cur.fetchall()
                    for emp_vac in emp_vac_all:
                        emp, vac = emp_vac
                        employers_vac_list.append(f"Работодатель {emp}: число вакансий {vac}")
        finally:
            conn.close()
        return employers_vac_list



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
for d in data:
    print(d)
