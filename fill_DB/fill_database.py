from classes.engine_HH import HH
import psycopg2
import os
from dotenv import load_dotenv


class FillDB:
    def __init__(self, employers_list):
        self.employers_list = employers_list

    def __get_employers(self):
        load_dotenv()
        for employer in self.employers_list:
            employer_info = HH(employer)
            employer_info.get_employer()
        employers = HH.employers_data
        return employers

    @staticmethod
    def __connect_to_db():
        load_dotenv()
        postgres_key = os.getenv('POSTGRESSQL_KEY')
        conn = psycopg2.connect(host='localhost', database='employers_db', user='postgres', password=postgres_key)
        return conn

    def fill_db(self):
        employers_id = []
        conn = self.__connect_to_db()
        employers = self.__get_employers()
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


fill_db_unit = FillDB(['skyeng', 'skillbox', 'лаборатория касперского', 'lesta games', 'VK', 'LG Electronics Inc.',
         'SberTech', 'YADRO', 'Доктор Веб', 'GeekBrains'])

fill_db_unit.fill_db()
