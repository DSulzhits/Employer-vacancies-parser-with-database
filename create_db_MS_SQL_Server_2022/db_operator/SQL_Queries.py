def create_database(database_name, size, maxsize, filegrowth):
    COMMAND = fr"""
            CREATE DATABASE {database_name}
            ON
            (
            NAME = {database_name}_data,
            FILENAME = 'T:\Program Files\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQL\DATA\{database_name}_data.mdf',
            SIZE = {size},
            MAXSIZE = {maxsize},
            FILEGROWTH={filegrowth}
            )
            LOG ON
            (NAME = {database_name}_log,
            FILENAME = 'T:\Program Files\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQL\DATA\{database_name}_data.ldf',
            SIZE = {size},
            MAXSIZE = {maxsize},
            FILEGROWTH = {filegrowth}
            )"""
    return COMMAND


def create_employers(table_name):
    QUERY = f"""CREATE TABLE {table_name}
            (employer_id int PRIMARY KEY, 
            employer_name nvarchar(100), 
            employer_url nvarchar(200))"""
    return QUERY


def create_vacancies(table_name):
    QUERY = f"""CREATE TABLE {table_name} 
            (vacancy_id int PRIMARY KEY, 
            vacancy_name nvarchar(100), 
            vacancy_url nvarchar(200), 
            vacancy_salary_from int, 
            vacancy_salary_to int, 
            employer_id int 
            REFERENCES employers(employer_id));"""
    return QUERY


def drop_table(table_name):
    QUERY = f"""DROP TABLE {table_name}"""
    return QUERY
