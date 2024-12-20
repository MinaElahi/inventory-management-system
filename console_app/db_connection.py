import pyodbc

server = 'localhost'  
database = 'BookInventoryDB'           

try:
    connection = pyodbc.connect(
        f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
    )
    print("Connection to database successful!")
except Exception as e:
    print("Error while connecting to database:", e)

