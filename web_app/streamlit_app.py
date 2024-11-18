import sys
import os
import streamlit as st
import sqlite3
from db_connection import create_books_table

# Ensure the database table is created
create_books_table()


def connect_db():
    try:
        # Connect to SQLite database
        # This file will be created in your project directory
        connection = sqlite3.connect("books_inventory.db")
        print("Connection to SQLite database successful")
        return connection
    except sqlite3.Error as e:
        print("Error while connecting to SQLite database:", e)
        return None


def main():
    st.title("Book Inventory Management System")
    menu = ["Add Book", "View All Books", "Filter Books",
            "Export to CSV", "Export to JSON"]
    choice = st.sidebar.selectbox("Menu", menu)
    st.write(f"You selected: {choice}")
    if choice == "Add Book":
        st.subheader("Add a New Book")
        title = st.text_input("Title")
        author = st.text_input("Author")
        genre = st.text_input("Genre")
        publication_date = st.date_input("Publication Date")
        isbn = st.text_input("ISBN")

        if st.button("Add Book"):
            try:
                connection = connect_db()
                cursor = connection.cursor()
                cursor.execute("""
                INSERT INTO Books (Title, Author, Genre, PublicationDate, ISBN)
                VALUES (?, ?, ?, ?, ?)
                """, (title, author, genre, publication_date, isbn))
                connection.commit()
                st.success(f"Book '{title}' added successfully!")
            except sqlite3.Error as e:
                st.error(f"Error adding book: {e}")
            finally:
                connection.close()

    elif choice == "View All Books":
        st.subheader("Books Inventory")
        try:
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Books")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    st.write(
                        f"**Title**: {row[1]}, **Author**: {row[2]}, **Genre**: {row[3]}, "
                        f"**Publication Date**: {row[4]}, **ISBN**: {row[5]}"
                    )
            else:
                st.info("No books found.")
        except sqlite3.Error as e:
            st.error(f"Error fetching books: {e}")
        finally:
            connection.close()

    elif choice == "Filter Books":
        st.subheader("Filter Books")
        filter_author = st.text_input("Enter Author's Name to Filter")

        if st.button("Search"):
            try:
                connection = connect_db()
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT * FROM Books WHERE Author = ?", (filter_author,))
                rows = cursor.fetchall()
                if rows:
                    for row in rows:
                        st.write(
                            f"Title: {row[1]}, Author: {row[2]}, Genre: {row[3]}, "
                            f"Publication Date: {row[4]}, ISBN: {row[5]}"
                        )
                else:
                    st.warning("No books found for the given author.")
            except sqlite3.Error as e:
                st.error(f"Error filtering books: {e}")
            finally:
                connection.close()

    elif choice == "Export to CSV":
        st.subheader("Export Books to CSV")
        try:
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Books")
            rows = cursor.fetchall()
            if rows:
                data_folder = os.path.join(os.path.dirname(__file__), 'data')
                os.makedirs(data_folder, exist_ok=True)
                with open(os.path.join(data_folder, "books_inventory.csv"), "w", encoding="utf-8") as file:
                    file.write(
                        "EntryID,Title,Author,Genre,PublicationDate,ISBN\n")
                    for row in rows:
                        file.write(",".join(map(str, row)) + "\n")
                st.success("Books exported to 'data/books_inventory.csv'!")
            else:
                st.warning("No data available to export.")
        except sqlite3.Error as e:
            st.error(f"Error exporting to CSV: {e}")
        finally:
            connection.close()

    elif choice == "Export to JSON":
        st.subheader("Export Books to JSON")
        try:
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Books")
            rows = cursor.fetchall()
            if rows:
                data_folder = os.path.join(os.path.dirname(__file__), 'data')
                os.makedirs(data_folder, exist_ok=True)
                books = []
                for row in rows:
                    books.append(
                        {
                            "EntryID": row[0],
                            "Title": row[1],
                            "Author": row[2],
                            "Genre": row[3],
                            "PublicationDate": str(row[4]),
                            "ISBN": row[5],
                        }
                    )
                with open(os.path.join(data_folder, "books_inventory.json"), "w") as file:
                    import json
                    json.dump(books, file, indent=4)
                st.success("Books exported to 'data/books_inventory.json'!")
            else:
                st.warning("No data available to export.")
        except sqlite3.Error as e:
            st.error(f"Error exporting to JSON: {e}")
        finally:
            connection.close()


if __name__ == "__main__":
    main()
