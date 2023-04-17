from classes.engine_HH import HH
import psycopg2
import os
from dotenv import load_dotenv


def fill_employers_db(employers_list):
    employers_id = []
    load_dotenv()
    postgres_key = os.getenv('POSTGRESSQL_KEY')
    for employer in employers_list:
        employer_info = HH(employer)
        employer_info.get_employer()
    employers = HH.employers_data

    conn = psycopg2.connect(host='localhost', database='employers_db', user='postgres', password=postgres_key)
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

#
# fill_DB(['skyeng', 'skillbox', 'лаборатория касперского', 'lesta games', 'VK', 'LG Electronics Inc.',
#          'SberTech', 'YADRO', 'Доктор Веб', 'GeekBrains'])
