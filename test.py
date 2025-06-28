import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
import json
import os

# File paths for storing data
BOOKS_FILE = 'books.json'
BORROWED_BOOKS_FILE = 'borrowed_books.json'
RETURNED_BOOKS_FILE = 'returned_books.json'
STUDENTS_FILE = 'students.json'
SEATS_FILE = 'seats.json'


root = tk.Tk()
root.title("Library Management System")
root.geometry("800x600")

#load and save data in variables for further uses 
def load_data():
    global books, borrowed_books, returned_books, students, seats
    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, 'r') as f:
            books = json.load(f)
    if os.path.exists(BORROWED_BOOKS_FILE):
        with open(BORROWED_BOOKS_FILE, 'r') as f:
            borrowed_books = json.load(f)
    if os.path.exists(RETURNED_BOOKS_FILE):
        with open(RETURNED_BOOKS_FILE, 'r') as f:
            returned_books = json.load(f)
    if os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, 'r') as f:
            students = json.load(f)
    if os.path.exists(SEATS_FILE):
        with open(SEATS_FILE, 'r') as f:
            seats = json.load(f)

def save_data():
    with open(BOOKS_FILE, 'w') as f:
        json.dump(books, f)
    with open(BORROWED_BOOKS_FILE, 'w') as f:
        json.dump(borrowed_books, f)
    with open(RETURNED_BOOKS_FILE, 'w') as f:
        json.dump(returned_books, f)
    with open(STUDENTS_FILE, 'w') as f:
        json.dump(students, f)
    with open(SEATS_FILE, 'w') as f:
        json.dump(seats, f)

# Initialize data
books = {}
borrowed_books = {}
returned_books = {}
students = {}
seats = {"A": [True]*10, "B": [True]*10, "C": [True]*10}  # True means seat is empty

# Load data from files
load_data()

# Book Management Functions
def add_book():
    book_id = book_id_entry.get()
    book_name = book_name_entry.get()
    quantity = quantity_entry.get()
    field = field_entry.get()
    
    if not book_id and not book_name:
        messagebox.showwarning("Input Error", "Please enter at least a book ID or book name.")
        return
    
    if not book_id:
        book_id = f"ID{len(books)+1:03d}"
    
    if not book_name:
        book_name = "Unknown"
    if not quantity:
        quantity = "Unknown"
    if not field:
        field = "Unknown"
    
    books[book_id] = {"name": book_name, "quantity": quantity, "field": field}
    save_data()
    messagebox.showinfo("Success", f"Book '{book_name}' added successfully.")
    clear_book_entries()

def search_book():
    book_id = book_id_entry.get()
    if book_id in books:
        book = books[book_id]
        book_info = f"Name: {book['name']}\nQuantity: {book['quantity']}\nField: {book['field']}"
        messagebox.showinfo("Book Found", book_info)
    else:
        messagebox.showwarning("Not Found", "Book not found.")

def delete_book():
    book_id = book_id_entry.get()
    if book_id in books:
        del books[book_id]
        save_data()
        messagebox.showinfo("Success", "Book deleted successfully.")
    else:
        messagebox.showwarning("Not Found", "Book not found.")
    clear_book_entries()

def clear_book_entries():
    book_id_entry.delete(0, tk.END)
    book_name_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    field_entry.delete(0, tk.END)

# Debt Management Functions
def borrow_book():
    student_id = student_id_entry.get()
    book_id = borrow_book_id_entry.get()
    if book_id in books and books[book_id]['quantity'] != "Unknown" and int(books[book_id]['quantity']) > 0:
        if student_id not in borrowed_books:
            borrowed_books[student_id] = []
        borrowed_books[student_id].append(book_id)
        books[book_id]['quantity'] = str(int(books[book_id]['quantity']) - 1)
        save_data()
        messagebox.showinfo("Success", f"Book '{books[book_id]['name']}' borrowed by student '{student_id}'.")
    else:
        messagebox.showwarning("Unavailable", "Book not available for borrowing.")
    clear_borrow_entries()

def return_book():
    student_id = student_id_entry.get()
    book_id = return_book_id_entry.get()
    if student_id in borrowed_books and book_id in borrowed_books[student_id]:
        borrowed_books[student_id].remove(book_id)
        if student_id not in returned_books:
            returned_books[student_id] = []
        returned_books[student_id].append(book_id)
        books[book_id]['quantity'] = str(int(books[book_id]['quantity']) + 1)
        save_data()
        messagebox.showinfo("Success", f"Book '{books[book_id]['name']}' returned by student '{student_id}'.")
    else:
        messagebox.showwarning("Error", "Invalid return attempt.")
    clear_return_entries()

def clear_borrow_entries():
    student_id_entry.delete(0, tk.END)
    borrow_book_id_entry.delete(0, tk.END)

def clear_return_entries():
    student_id_entry.delete(0, tk.END)
    return_book_id_entry.delete(0, tk.END)

# Student Entry/Exit Functions
def check_in_student():
    student_id = student_id_entry.get()
    check_in_time = datetime.datetime.now().isoformat()
    students[student_id] = check_in_time
    save_data()
    messagebox.showinfo("Checked In", f"Student '{student_id}' checked in at {check_in_time}")
    clear_student_entries()

def check_out_student():
    student_id = student_id_entry.get()
    if student_id in students:
        check_in_time = datetime.datetime.fromisoformat(students[student_id])
        check_out_time = datetime.datetime.now()
        time_spent = check_out_time - check_in_time
        hours_spent = time_spent.total_seconds() / 3600
        messagebox.showinfo("Checked Out", f"Student '{student_id}' checked out. Time spent: {hours_spent:.2f} hours.")
        del students[student_id]
        save_data()
    else:
        messagebox.showwarning("Error", "Student not found.")
    clear_student_entries()

def clear_student_entries():
    student_id_entry.delete(0, tk.END)

# Seat Management Functions
def add_seats():
    row = seat_row_entry.get()
    num_seats = int(num_seats_entry.get())
    seats[row] = [True] * num_seats
    save_data()
    messagebox.showinfo("Success", f"Added {num_seats} seats in row '{row}'")
    clear_seat_entries()

def find_empty_seat():
    row = seat_row_entry.get()
    if row in seats:
        empty_seats = [index for index, seat in enumerate(seats[row]) if seat]
        messagebox.showinfo("Empty Seats", f"Empty seats in row '{row}': {empty_seats}")
    else:
        messagebox.showwarning("Error", "Row not found.")
    clear_seat_entries()

def clear_seat_entries():
    seat_row_entry.delete(0, tk.END)
    num_seats_entry.delete(0, tk.END)

# Creating GUI Elements
# Book Management GUI
book_frame = tk.LabelFrame(root, text="Book Management")
book_frame.pack(fill="both", expand="yes", padx=10, pady=10)

tk.Label(book_frame, text="Book ID:").grid(row=0, column=0, padx=5, pady=5)
book_id_entry = tk.Entry(book_frame)
book_id_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(book_frame, text="Book Name:").grid(row=1, column=0, padx=5, pady=5)
book_name_entry = tk.Entry(book_frame)
book_name_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(book_frame, text="Quantity:").grid(row=2, column=0, padx=5, pady=5)
quantity_entry = tk.Entry(book_frame)
quantity_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(book_frame, text="Field:").grid(row=3, column=0, padx=5, pady=5)
field_entry = tk.Entry(book_frame)
field_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Button(book_frame, text="Add Book", command=add_book).grid(row=4, column=0, padx=5, pady=5)
tk.Button(book_frame, text="Search Book", command=search_book).grid(row=4, column=1, padx=5, pady=5)
tk.Button(book_frame, text="Delete Book", command=delete_book).grid(row=4, column=2, padx=5, pady=5)

# Debt Management GUI
debt_frame = tk.LabelFrame(root, text="Debt Management")
debt_frame.pack(fill="both", expand="yes", padx=10, pady=10)

tk.Label(debt_frame, text="Student ID:").grid(row=0, column=0, padx=5, pady=5)
student_id_entry = tk.Entry(debt_frame)
student_id_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(debt_frame, text="Book ID to Borrow:").grid(row=1, column=0, padx=5, pady=5)
borrow_book_id_entry = tk.Entry(debt_frame)
borrow_book_id_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Button(debt_frame, text="Borrow Book", command=borrow_book).grid(row=2, column=0, padx=5, pady=5)
tk.Label(debt_frame, text="Book ID to Return:").grid(row=3, column=0, padx=5, pady=5)
return_book_id_entry = tk.Entry(debt_frame)
return_book_id_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Button(debt_frame, text="Return Book", command=return_book).grid(row=4, column=0, padx=5, pady=5)

# Student Entry/Exit Management GUI
student_frame = tk.LabelFrame(root, text="Student Entry/Exit Management")
student_frame.pack(fill="both", expand="yes", padx=10, pady=10)

tk.Label(student_frame, text="Student ID:").grid(row=0, column=0, padx=5, pady=5)
student_id_entry = tk.Entry(student_frame)
student_id_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Button(student_frame, text="Check-In", command=check_in_student).grid(row=1, column=0, padx=5, pady=5)
tk.Button(student_frame, text="Check-Out", command=check_out_student).grid(row=1, column=1, padx=5, pady=5)

# Seat Management GUI
seat_frame = tk.LabelFrame(root, text="Seat Management")
seat_frame.pack(fill="both", expand="yes", padx=10, pady=10)

tk.Label(seat_frame, text="Seat Row:").grid(row=0, column=0, padx=5, pady=5)
seat_row_entry = tk.Entry(seat_frame)
seat_row_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(seat_frame, text="Number of Seats:").grid(row=1, column=0, padx=5, pady=5)
num_seats_entry = tk.Entry(seat_frame)
num_seats_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Button(seat_frame, text="Add Seats", command=add_seats).grid(row=2, column=0, padx=5, pady=5)
tk.Button(seat_frame, text="Find Empty Seats", command=find_empty_seat).grid(row=2, column=1, padx=5, pady=5)

root.mainloop()
