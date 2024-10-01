import os
import json
import pyodbc
from dotenv import load_dotenv
from create_db_MS_SQL_Server_2022.db_operator.operate_tables import ConnectDB
import SQL_Queries


class DBManager:

    def __init__(self, connector_obj):
        self.conn = connector_obj

    @staticmethod
    def get_data_from_json(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            python_data = json.load(file)
            return python_data

    def fill_table(self, database_name, table_name, filename, sql_query):
        cursor = self.conn.cursor()
        cursor.execute(f"USE {database_name}")
        data_to_fill_list = self.get_data_from_json(filename)
        try:
            for data_to_fill in data_to_fill_list:
                cursor.execute(sql_query(table_name, data_to_fill))
        except pyodbc.Error as ex:
            return ex
        else:
            return "Данные помещены в таблицу"


if __name__ == "__main__":
    load_dotenv()
    SERVER = os.getenv('MS_SQL_SERVER')
    DATABASE = os.getenv('MS_SQL_DATABASE')
    USER = os.getenv('MS_SQL_USER')
    PASSWORD = os.getenv('MS_SQL_KEY')
    active_db = "EmployersVacancies"

    my_conn = ConnectDB.connect_to_db(SERVER, DATABASE, USER, PASSWORD)
    my_manager = DBManager(my_conn)
    print(my_manager.fill_table(active_db, 'Employers', r'data\employers.json', SQL_Queries.fill_employers))
    print(my_manager.fill_table(active_db, 'Vacancies', r'data\vacancies.json', SQL_Queries.fill_vacancies))
