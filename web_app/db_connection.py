import sqlite3

def create_books_table():
    try:
        connection = sqlite3.connect("books_inventory.db")
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Books (
            EntryID INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT NOT NULL,
            Author TEXT NOT NULL,
            Genre TEXT NOT NULL,
            PublicationDate TEXT NOT NULL,
            ISBN TEXT NOT NULL UNIQUE
        )
        """)
        connection.commit()
        connection.close()
        print("Books table created successfully.")
    except sqlite3.Error as e:
        print("Error creating Books table:", e)
