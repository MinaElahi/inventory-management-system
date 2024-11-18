import pyodbc
import csv
from datetime import datetime
import json
import unittest


connection = pyodbc.connect(
    "DRIVER={SQL Server};SERVER=localhost;DATABASE=bookInventoryDB;Trusted_Connection=yes;"
)

cursor = connection.cursor()
# Function Definition

class TestInventoryManagement(unittest.TestCase):
    def test_validate_date(self):
        self.assertTrue(validate_date("2023-11-16"))
        self.assertFalse(validate_date("2023-02-30"))
        
def add_new_book(title, author, genre, publication_date, isbn):
    try:
        # Validate the publication date
        try:
            valid_date = datetime.strptime(publication_date, "%Y-%m-%d")
        except ValueError:
            print(
                "Invalid date format or invalid date. Please enter a valid date in YYYY-MM-DD format.")
            return

        # Check if the ISBN already exists
        cursor.execute("SELECT * FROM Books WHERE ISBN = ?", (isbn,))
        existing_book = cursor.fetchone()
        if existing_book:
            print(f"Book with ISBN {isbn} already exists in the database!")
            return

        # Insert the book into the database
        cursor.execute(
            """
            INSERT INTO Books (Title, Author, Genre, PublicationDate, ISBN)
            VALUES (?, ?, ?, ?, ?)
            """,
            (title, author, genre, publication_date, isbn),
        )
        connection.commit()
        print(f"Book '{title}' added successfully!")
    except Exception as e:
        print("Error while adding the book: ", e)


def view_all_books():
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM Books"
        cursor.execute(query)

        rows = cursor.fetchall()  # Fetch all rows

        print("Books in the Inventory: ")
        for row in rows:
            print(f"EntryID: {row.EntryID}, Title: {row.Title}, Author: {row.Author}, Genre: {row.genre}, Publication Date: {row.PublicationDate}, ISBN: {row.ISBN}")
    except Exception as e:
        print("Error while fetching books: ", e)


def filter_books_by_author(author_name):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM Books WHERE Author = ?"
        cursor.execute(query, (author_name,))

        rows = cursor.fetchall()  # Fetch all matching rows
        if rows:
            print(f"Books by {author_name}:")
            for row in rows:
                print(f"EntryID: {row[0]}, Title: {row[1]}, Genre: {row[3]}, "
                      f"PublicationDate: {row[4]}, ISBN: {row[5]}")
        else:
            print(f"No books found for the author: {author_name}")
    except Exception as e:
        print("Error while filtering books: ", e)

def filter_books_by_year(year):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM Books WHERE YEAR(PublicationDate) >= ?"
        cursor.execute(query, (year,))
        rows = cursor.fetchall()

        if rows:
            print(f"Books published after {year}:")
            for row in rows:
                print(f"EntryID: {row[0]}, Title: {row[1]}, Author: {row[2]}, Genre: {row[3]}, PublicationDate: {row[4]}, ISBN: {row[5]}")
        else:
            print(f"No books found published after {year}.")
    except Exception as e:
        print("Error while filtering books by year: ", e)
def delete_book_by_isbn(isbn):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM Books WHERE ISBN = ?"
        cursor.execute(query, (isbn,))
        connection.commit()
        print(f"Book with ISBN {isbn} deleted successfully!")
    except Exception as e:
        print("Error while deleting the book: ", e)
def update_book_title(isbn, new_title):
    try:
        cursor = connection.cursor()
        query = "UPDATE Books SET Title = ? WHERE ISBN = ?"
        cursor.execute(query, (new_title, isbn))
        connection.commit()
        print(f"Book with ISBN {isbn} updated successfully!")
    except Exception as e:
        print("Error while updating the book: ", e)

def export_books_to_csv():
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM Books"
        cursor.execute(query)

        rows = cursor.fetchall()
        column_names = [desc[0]
                        for desc in cursor.description]  # Get column names

        # Write to a CSV file
        with open('books_inventory.csv', 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(column_names)  
            writer.writerows(rows)        

        print("Books data exported successfully to 'books_inventory.csv'!")
    except Exception as e:
        print("Error while exporting books to CSV:", e)


def export_books_to_json():
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM Books"
        cursor.execute(query)

        rows = cursor.fetchall()  # Fetch all rows

        # Extract column names
        column_names = [desc[0] for desc in cursor.description]

        # Convert rows to a list of dictionaries
        books = [dict(zip(column_names, row)) for row in rows]

        # Write to a JSON file
        with open("books_inventory.json", "w", encoding="utf-8") as json_file:
            json.dump(books, json_file, indent=4, ensure_ascii=False)

        print("Books data exported successfully to 'books_inventory.json'!")
    except Exception as e:
        print("Error while exporting books to JSON: ", e)

def validate_date(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False    
# Main function to run the menu


def main():
    while True:
        print("\nInventory Management System")
        print("1. Add a New Book")
        print("2. View All Books")
        print("3. Filter Books by Author")
        print("4. Export Books to CSV")
        print("5. Export Books to JSON")
        print("6. Exit")
        print("\nEnter your choice: ", end="")
        choice = input().strip()

        if choice == "1":
            # Add a new book
            title = input("Enter book title: ").strip()
            author = input("Enter author name: ").strip()
            genre = input("Enter genre: ").strip()
            publication_date = input(
                "Enter publication date (YYYY-MM-DD): ").strip()
            isbn = input("Enter ISBN: ").strip()

            add_new_book(
                title=title,
                author=author,
                genre=genre,
                publication_date=publication_date,
                isbn=isbn
            )

        elif choice == "2":
            # View all books
            view_all_books()

        elif choice == "3":
            # Filter books by author
            author_name = input("Enter author name to filter: ").strip()
            filter_books_by_author(author_name)

        elif choice == "4":
            # Export books to CSV
            export_books_to_csv()
            print("Books exported to 'books_inventory.csv'.")
        elif choice == "5":
            export_books_to_json()
            print("Books exported to 'books_inventory.json'.")
        elif choice == "6":
            # Exit
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid option.")

        # Pause before showing the menu again
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()

connection.close()
