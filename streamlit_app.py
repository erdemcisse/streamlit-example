import streamlit as st
import pandas as pd
import sqlite3

# Function to connect to the database
def init_db(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_name TEXT,
            book_no TEXT,
            student_name TEXT,
            matrikel_number TEXT
        );
    """)
    conn.commit()

# Function to add a new entry to the database
def add_book(conn, book_name, book_no, student_name, matrikel_number):
    conn.execute("""
        INSERT INTO books (book_name, book_no, student_name, matrikel_number)
        VALUES (?, ?, ?, ?);
    """, (book_name, book_no, student_name, matrikel_number))
    conn.commit()

# Function to delete an entry from the database
def delete_book(conn, book_id):
    conn.execute("DELETE FROM books WHERE id = ?;", (book_id,))
    conn.commit()

# Function to get all book entries from the database
def get_all_books(conn):
    cursor = conn.execute("SELECT * FROM books;")
    data = cursor.fetchall()
    return data

# Initialize the database
conn = sqlite3.connect('library.db')
init_db(conn)

# Streamlit UI
st.title("Library Management System MVP")

# Input form
with st.form("book_form", clear_on_submit=True):
    book_name = st.text_input("Book Name")
    book_no = st.text_input("Book No")
    student_name = st.text_input("Student Name")
    matrikel_number = st.text_input("Matrikel Number")
    submit_button = st.form_submit_button("Add Book")

if submit_button:
    add_book(conn, book_name, book_no, student_name, matrikel_number)
    st.success("Book added successfully!")

# Display books in a table
books = get_all_books(conn)
books_df = pd.DataFrame(books, columns=["ID", "Book Name", "Book No", "Student Name", "Matrikel Number"])
st.write(books_df)

# Delete book
book_id_to_delete = st.selectbox("Select a Book ID to delete", [book[0] for book in books])
if st.button("Delete Book"):
    delete_book(conn, book_id_to_delete)
    st.success(f"Book with ID {book_id_to_delete} deleted successfully!")
    st.experimental_rerun()

# Close the database connection when the script completes
conn.close()
