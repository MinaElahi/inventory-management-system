import pyodbc

server = 'localhost'  # Your server name from the screenshot
database = 'BookInventoryDB'           # Your database name

try:
    connection = pyodbc.connect(
        f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
    )
    print("Connection to database successful!")
except Exception as e:
    print("Error while connecting to database:", e)

