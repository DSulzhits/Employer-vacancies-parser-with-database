from classes.engine_HH import HH
import psycopg2
import os
from dotenv import load_dotenv


class ConnectDB:
    @staticmethod
    def connect_to_db():
        load_dotenv()
        postgres_key = os.getenv('POSTGRESSQL_KEY')
        conn = psycopg2.connect(host='localhost', database='employers_db', user='postgres', password=postgres_key)
        return conn


class FillDB(HH):
    employers_names = []

    def __init__(self, employers_list):
        self.employers_list = employers_list
        for employer in self.employers_list:
            super().__init__(employer)
            self.employers_names.append(self.employer)

    @classmethod
    def __get_employers_all(cls):
        for employer in cls.employers_names:
            employer_info = HH(employer)
            employer_info.get_employer()
        return super().employers_data

    @classmethod
    def __get_vacancies_all(cls):
        vacancies_all = []
        for employer in cls.employers_data:
            emp = HH(employer['name'])
            vacancies_emp = emp.get_vacancies(employer['id'])
            for vacancy in vacancies_emp:
                vacancies_all.append(vacancy)
        return vacancies_all

    # @staticmethod
    # def __connect_to_db():
    #     load_dotenv()
    #     postgres_key = os.getenv('POSTGRESSQL_KEY')
    #     conn = psycopg2.connect(host='localhost', database='employers_db', user='postgres', password=postgres_key)
    #     return conn

    def fill_db_employers(self):
        employers_id = []
        conn = ConnectDB.connect_to_db()
        employers = self.__get_employers_all()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM employers")
                    rows = cur.fetchall()
                    for row in rows:
                        emp_id, name, url = row
                        employers_id.append(emp_id)
                    for employer in employers:
                        if int(employer['id']) not in employers_id:
                            cur.execute('INSERT INTO employers VALUES (%s, %s, %s)',
                                        (employer['id'],
                                         employer['name'],
                                         employer['alternate_url']))
                        else:
                            print(f"Работодатель {employer['name']} id {employer['id']} уже существует")
        finally:
            conn.close()

    def fill_db_vacancies(self):
        vacancies_id = []
        conn = ConnectDB.connect_to_db()
        vacancies = self.__get_vacancies_all()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM vacancies")
                    rows = cur.fetchall()
                    for row in rows:
                        vac_id, vac_name, vac_url, vac_from, vac_to, vac_emp_id = row
                        vacancies_id.append(vac_id)
                    for vacancy in vacancies:
                        if int(vacancy['id']) not in vacancies_id:
                            cur.execute('INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s)',
                                        (vacancy['id'], vacancy['vacancy'], vacancy['url'], vacancy['salary_from'],
                                         vacancy['salary_to'], vacancy['employer_id']))
                        else:
                            print(f"Вакансия {vacancy['vacancy']} id {vacancy['id']} уже существует")
        finally:
            conn.close()

# fill_db_unit = FillDB(['skyeng', 'skillbox', 'лаборатория касперского', 'lesta games', 'Вконтакте', 'LG Electronics Inc.',
#                        'SberTech', 'YADRO', 'Доктор Веб', 'GeekBrains'])

# fill_db_unit.fill_db_employers()
# fill_db_unit.fill_db_vacancies()
