import os
import pyodbc
from dotenv import load_dotenv
import SQL_Queries


class ConnectDB:
    @staticmethod
    def connect_to_db(server, database, user, password):
        connectionString = f'''DRIVER={{ODBC Driver 18 for SQL Server}};
                               SERVER={server};
                               DATABASE={database};
                               UID={user};
                               PWD={password}'''
        try:
            conn = pyodbc.connect(connectionString)
            conn.autocommit = True
        except pyodbc.ProgrammingError as ex:
            print(ex)
        else:
            return conn


class MSSqlDBOperator:

    def __init__(self, connector_obj):
        self.conn = connector_obj

    def create_database(self, database_name, size, maxsize, filegrowth):
        SQL_COMMAND = SQL_Queries.create_database(database_name, size, maxsize, filegrowth)
        try:
            self.conn.execute(SQL_COMMAND)
        except pyodbc.ProgrammingError as ex:
            return ex
        else:
            return f"База данных: {database_name} создана"

    def create_tables(self, database_name, table_name, sql_query):
        cursor = self.conn.cursor()
        cursor.execute(f"USE {database_name}")
        SQL_QUERY = sql_query(table_name)
        try:
            cursor.execute(SQL_QUERY)
        except pyodbc.ProgrammingError as ex:
            return ex
        else:
            return f"Таблица: {table_name} успешно создана!"

    def drop_tables(self, database_name, table_name, sql_query):
        cursor = self.conn.cursor()
        cursor.execute(f"USE {database_name}")
        SQL_QUERY = sql_query(table_name)
        try:
            cursor.execute(SQL_QUERY)
        except pyodbc.ProgrammingError as ex:
            return ex
        else:
            return f"Таблица: {table_name} успешно удалена!"


if __name__ == "__main__":
    load_dotenv()
    SERVER = os.getenv('MS_SQL_SERVER')
    DATABASE = os.getenv('MS_SQL_DATABASE')
    USER = os.getenv('MS_SQL_USER')
    PASSWORD = os.getenv('MS_SQL_KEY')
    new_db = "EmployersVacancies"

    my_conn = ConnectDB.connect_to_db(SERVER, DATABASE, USER, PASSWORD)
    my_db = MSSqlDBOperator(my_conn)
    print(my_db.create_database(new_db, "10MB", "20GB", "5%"))
    print(my_db.drop_tables(new_db, "Vacancies", SQL_Queries.drop_table))
    print(my_db.drop_tables(new_db, "Employers", SQL_Queries.drop_table))
    print(my_db.create_tables(new_db, "Employers", SQL_Queries.create_employers))
    print(my_db.create_tables(new_db, "Vacancies", SQL_Queries.create_vacancies))
