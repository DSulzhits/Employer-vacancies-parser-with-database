import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()
SERVER = os.getenv('MS_SQL_SERVER')
DATABASE = os.getenv('MS_SQL_DATABASE')
USER = os.getenv('MS_SQL_USER')
PASSWORD = os.getenv('MS_SQL_KEY')

# """SimpleConnection"""
# connectionString = f'''DRIVER={{SQL Server}};
#                                SERVER={SERVER};
#                                DATABASE={DATABASE};
#                                Trusted_Connection=yes'''

"""SecureConnection"""
connectionString = f'''DRIVER={{ODBC Driver 17 for SQL Server}};
                               SERVER={SERVER};
                               DATABASE={DATABASE};
                               UID={USER};
                               PWD={PASSWORD}'''

"""CreateDBParams"""
SQL_COMMAND = r"""
CREATE DATABASE TestDatabase
ON
(
  NAME = TestDatabase_data,
  FILENAME = 'T:\Program Files\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQL\DATA\TestDatabase_data.mdf',
  SIZE = 10MB,
  MAXSIZE = 100GB,
  FILEGROWTH = 5%
 )
LOG ON
(
  NAME = 'TestDatabase_log',
  FILENAME = 'T:\Program Files\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQL\DATA\TestDatabase_data.ldf',
  SIZE = 5MB,
  MAXSIZE = 10GB,
  FILEGROWTH = 5%
 )"""
conn = pyodbc.connect(connectionString)
conn.autocommit = True
try:
    conn.execute(SQL_COMMAND)
except pyodbc.Error as ex:
    print(ex)
else:
    print("Database Created")
finally:
    conn.close()

SQL_QUERY = f"""
    CREATE TABLE dbo.MyTestTable
    (EmployerId int PRIMARY KEY,
    EmployerName nvarchar(100),
    EmployerUrl nvarchar(200));
"""


# SQL_QUERY = f"""
# IF OBJECT_ID(N'MyTestTable', N'U') IS NULL
# BEGIN
#     CREATE TABLE dbo.MyTestTable
#     (EmployerId int PRIMARY KEY,
#     EmployerName nvarchar(100),
#     EmployerUrl nvarchar(200))
# END;"""

conn = pyodbc.connect(connectionString)
conn.autocommit = True
cursor = conn.cursor()
try:
    cursor.execute("USE TestDatabase")
    cursor.execute(SQL_QUERY)
except pyodbc.ProgrammingError as ex:
    print(ex)
except pyodbc.Error as ex:
    print(ex)
else:
    print("Table Created")
finally:
    conn.close()

SQL_QUERY = """
SELECT LastName, FirstName
FROM Students
"""
records_list = []
conn = pyodbc.connect(connectionString)
conn.autocommit = True
cursor = conn.cursor()
try:
    cursor.execute("USE Academy")
    cursor.execute(SQL_QUERY)
    records = cursor.fetchall()
except pyodbc.ProgrammingError as ex:
    print(ex)
except pyodbc.Error as ex:
    print(ex)
else:
    print("Data Recieved")
    for record in records:
        print(f"{record.LastName}\t{record.FirstName}")
        result = {"last_name": record.LastName, "first_name": record.FirstName}
        records_list.append(result)
finally:
    conn.close()

print(records_list)