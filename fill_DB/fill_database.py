from classes.engine_HH import HH
import psycopg2
import os
import csv
from dotenv import load_dotenv

load_dotenv()
postgres_key = os.getenv('POSTGRESSQL_KEY')


def fill_DB(employer):
    employer = HH(employer)
    employer_data = employer.get_request()
    employer_vacancies = employer_data.get_vacancies()
    conn = psycopg2.connect(host='localhost', database='employers_db', user='postgres', password=postgres_key)
    try:
        with conn.cursor() as cur:
            for vacancy in range(len(employer_vacancies)):
                cur.execute(f'INSERT INTO  {employer}  VALUES (%, %, %, %, %, %)', (vacancy['employer']))


    finally:
        conn.close()
