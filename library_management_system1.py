import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# Database connection
conn = sqlite3.connect("library.db")
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_name TEXT NOT NULL,
    author TEXT NOT NULL,
    issued_by TEXT DEFAULT 'None',
    issue_date TEXT DEFAULT 'None',
    due_date TEXT DEFAULT 'None'
)
''')
conn.commit()
conn.close()

# Function to add a book
def add_book():
    book_name = book_name_entry.get()
    author = author_entry.get()

    if not book_name or not author:
        messagebox.showerror("Error", "Please fill all fields")
        return

    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (book_name, author) VALUES (?, ?)", (book_name, author))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Book Added Successfully")
    view_books()

# Function to view books
def view_books():
    for item in tree.get_children():
        tree.delete(item)

    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", "end", values=row)

# Function to delete a book
def delete_book():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a book")
        return

    book_id = tree.item(selected_item)['values'][0]

    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Book Deleted Successfully")
    view_books()

# Function to issue a book
def issue_book():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a book")
        return

    book_id = tree.item(selected_item)['values'][0]
    issued_by = issued_by_entry.get()
    due_date = due_date_entry.get()
    issue_date = datetime.now().strftime("%d-%m-%Y")

    if not issued_by or not due_date:
        messagebox.showerror("Error", "Please fill all fields")
        return

    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET issued_by=?, issue_date=?, due_date=? WHERE id= ?", 
                   (issued_by, issue_date, due_date, book_id))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Book Issued Successfully")
    view_books()

# UI Setup
root = tk.Tk()
root.title("Library Management System")
root.geometry("1000x600")

# Book Details
book_name_label = tk.Label(root, text="Book Name:")
book_name_label.pack()
book_name_entry = tk.Entry(root)
book_name_entry.pack()

author_label = tk.Label(root, text="Author:")
author_label.pack()
author_entry = tk.Entry(root)
author_entry.pack()

add_button = tk.Button(root, text="Add Book", command=add_book)
add_button.pack()

# Treeview with gradual column expansion
columns = ["ID", "Book Name", "Author", "Issued By", "Issue Date", "Due Date"]
tree = ttk.Treeview(root, columns=columns, show="headings")

for i, col in enumerate(columns):
    tree.heading(col, text=col)
    tree.column(col, width=0)

# Function to expand columns one by one
def expand_columns():
    for i in range(len(columns)):
        tree.column(columns[i], width=150)
        root.update()
        root.after(500)

expand_columns()
tree.pack()

view_button = tk.Button(root, text="View Books", command=view_books)
view_button.pack()

delete_button = tk.Button(root, text="Delete Book", command=delete_book)
delete_button.pack()

# Issue Book Section
issued_by_label = tk.Label(root, text="Issued By:")
issued_by_label.pack()
issued_by_entry = tk.Entry(root)
issued_by_entry.pack()

due_date_label = tk.Label(root, text="Due Date (DD-MM-YYYY):")
due_date_label.pack()
due_date_entry = tk.Entry(root)
due_date_entry.pack()

issue_button = tk.Button(root, text="Issue Book", command=issue_book)
issue_button.pack()

view_books()
root.mainloop()