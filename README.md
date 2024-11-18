# Inventory Management System

A simple inventory management system for books.

## Inventory Management System

This is a Python-based Inventory Management System for books that includes a console application and a web application. The system allows users to add new books, filter books based on various criteria, and export data to CSV or JSON formats.

---

## Table of Contents

- Features
- Technologies Used
- Setup Instructions
  - Console Application Setup
  - Web Application Setup
- Sample Data
- How to Use
- File Structure
- Acknowledgments

---

## Features

- **Add Books**: Add new books to the inventory.
- **View All Books**: Display a list of all books in the inventory.
- **Filter Books**: Search for books by author.
- **Export Data**: Export book inventory to CSV or JSON formats.
- **Console App**: Interact with the system via the console.
- **Web App**: Use a user-friendly web interface.

---

## Technologies Used

- Python 3.11
- **SQLite** (for the web application)
- **Microsoft SQL Server** (for the console application)
- **Streamlit** (for the web interface)
- **Git** (version control)

---

## Setup Instructions

### Console Application Setup

1. Ensure Microsoft SQL Server is installed on your system.
2. Open **SQL Server Management Studio (SSMS)**.
3. Create a new database (e.g., `BookInventoryDB`).
4. Execute the SQL script in `sql/books_inventory.sql` to set up the schema and insert sample data:
   ```sql
   USE BookInventoryDB;
   CREATE TABLE Books (
       EntryID INT PRIMARY KEY IDENTITY(1,1),
       Title NVARCHAR(255) NOT NULL,
       Author NVARCHAR(255) NOT NULL,
       Genre NVARCHAR(100),
       PublicationDate DATE,
       ISBN NVARCHAR(13)
   );
   INSERT INTO Books (Title, Author, Genre, PublicationDate, ISBN)
   VALUES
   ('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', '1925-04-10', '9780743273565'),
   ('1984', 'George Orwell', 'Dystopian', '1949-06-08', '9780451524935');
