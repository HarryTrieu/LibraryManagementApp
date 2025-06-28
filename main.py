import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
import json
import os

BOOKS = 'books.json'
BORROWED_BOOKS = 'borrowed_books.json'
RETURNED_BOOKS = 'returned_books.json'
STUDENTS_FILE = 'students.json'
SEATS_FILE = 'seats.json'

books = {}
borrowed_books = {}
returned_books = {}
students = {}
seats = {"A": [True]*10, "B": [True]*10, "C": [True]*10} #True is available,Fasle means not.

#functions 
def load_data():
    global books, borrowed_books, returned_books, students, seats
    if os.path.exists(BOOKS):
        with open(BOOKS, 'r') as f:
            books = json.load(f)
    if os.path.exists(BORROWED_BOOKS):
        with open(BORROWED_BOOKS, 'r') as f:
            borrowed_books = json.load(f)
    if os.path.exists(RETURNED_BOOKS):
        with open(RETURNED_BOOKS, 'r') as f:
            returned_books = json.load(f)
    if os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, 'r') as f:
            students = json.load(f)
    if os.path.exists(SEATS_FILE):
        with open(SEATS_FILE, 'r') as f:
            seats = json.load(f)
            
def save_data():
    with open(BOOKS, 'w') as f:
        json.dump(books, f)
    with open(BORROWED_BOOKS, 'w') as f:
        json.dump(borrowed_books, f)
    with open(RETURNED_BOOKS, 'w') as f:
        json.dump(returned_books, f)
    with open(STUDENTS_FILE, 'w') as f:
        json.dump(students, f)
    with open(SEATS_FILE, 'w') as f:
        json.dump(seats, f)

def add_book():
    book_id = book_id_entry.get()
    book_name = book_name_entry.get()
    field = field_entry.get()
    
    if not book_id or not book_name:
        messagebox.showwarning("Input Error", "Please enter both book ID and book name.")
        return
    
    if book_id in books:
        messagebox.showwarning("Duplicate ID", "Book ID already exists. Please enter a unique ID.")
        return
    
    books[book_id] = {"name": book_name, "status": "Available", "field": field}
    save_data()
    messagebox.showinfo("Success", f"Book '{book_name}' added successfully.")
    clear_book_entries()
    
def search_book():
    book_id = book_id_entry.get()
    if book_id in books:
        book_info = f"Name: {books[book_id]['name']}\nStatus: {books[book_id].get('status', 'Unknown')}\nField: {books[book_id]['field']}"
        messagebox.showinfo("Book Found", book_info)
    else:
        messagebox.showwarning("Not Found", "Book not found.")

def delete_book():
    book_id = book_id_entry.get()
    if book_id in books:
        del books[book_id]
        save_data()
        messagebox.showinfo("Success", "Book deleted successfully.")
        clear_book_entries()
    else:
        messagebox.showwarning("Not Found", "Book not found.")
        
def clear_book_entries():
    book_id_entry.delete(0, tk.END)
    book_name_entry.delete(0, tk.END)
    field_entry.delete(0, tk.END)

# Debt Management Functions
def borrow_book():
    student_id = student_id_entry.get()
    book_id = borrow_book_id_entry.get()
    if book_id in books and books[book_id]['status'] == "Available":
        if student_id not in borrowed_books:
            borrowed_books[student_id] = []
        borrowed_books[student_id].append(book_id)
        books[book_id]['status'] = "Borrowed"
        save_data()
        messagebox.showinfo("Success", f"Book '{books[book_id]['name']}' borrowed by student '{student_id}'.")
        clear_borrow_entries()
    else:
        messagebox.showwarning("Unavailable", "Book not available for borrowing.")

def return_book():
    student_id = student_id_entry.get()
    book_id = return_book_id_entry.get()
    if student_id in borrowed_books and book_id in borrowed_books[student_id]:
        borrowed_books[student_id].remove(book_id)
        if student_id not in returned_books:
            returned_books[student_id] = []
        returned_books[student_id].append(book_id)
        books[book_id]['status'] = "Available"
        save_data()
        messagebox.showinfo("Success", f"Book '{books[book_id]['name']}' returned by student '{student_id}'.")
        clear_return_entries()
    else:
        messagebox.showwarning("Error", "Invalid return attempt.")

def clear_borrow_entries():
    student_id_entry.delete(0, tk.END)
    borrow_book_id_entry.delete(0, tk.END)

def clear_return_entries():
    student_id_entry.delete(0, tk.END)
    return_book_id_entry.delete(0, tk.END)

# Seat Management Functions
def add_seats():
    row = seat_row_entry.get()
    num_seats = int(num_seats_entry.get())
    if row not in seats:
        seats[row] = [True] * num_seats
        save_data()
        messagebox.showinfo("Success", f"Added {num_seats} seats in row '{row}'")
    else:
        messagebox.showwarning("Error", f"Row '{row}' already exists.")
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

#Display books function
def books_saved():
    # Clear the root window before displaying books
    for widget in root.winfo_children():
        widget.destroy()

    # Load data if not already loaded
    load_data()

    # Display books
    if books:
        for book_id, book_info in books.items():
            book_label = tk.Label(root, text=f"Book ID: {book_id}\nName: {book_info['name']}\nStatus: {book_info.get('status', 'Unknown')}\nField: {book_info['field']}", font=("Arial", 12))
            book_label.pack(padx=20, pady=10, anchor="w")
    else:
        no_books_label = tk.Label(root, text="No books available.", font=("Arial", 12))
        no_books_label.pack(padx=20, pady=10)


def display_books():
    # Define canvas and scrollbar as global variables
    global canvas, scrollbar

    root.geometry("1200x800")
    root.title("Books List")

    main_frame = ttk.Frame(root, padding=(20, 20, 20, 0))
    main_frame.pack(fill="both", expand=True)

    label = ttk.Label(main_frame, text="Books List", font=("Arial", 20))
    label.pack(pady=(0, 10))

    # Create a canvas to contain the book labels
    canvas = tk.Canvas(main_frame)
    canvas.pack(side="left", fill="both", expand=True)

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Configure the canvas to work with the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to hold the book labels
    frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    # Display the list of books in the frame
    books_saved()

    # Update the scroll region of the canvas
    frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

    # Bind mousewheel scrolling to the canvas
    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

    # Add a button to return to the previous page
    back_button = ttk.Button(main_frame, text="Back", command=go_back)
    back_button.pack(pady=(10, 20))

    # Add a button to refresh the books list
    refresh_button = ttk.Button(main_frame, text="Refresh", command=books_saved)
    refresh_button.pack(pady=(10, 20))

def go_back():
    # Destroy the canvas and its children
    canvas.destroy()

    # Recreate the previous page
    






        
#GUI ------------------------------------------------------------------------------------------------------------------
root = tk.Tk()
#HEader
root.geometry("1000x700")
root.title("Librabry management")

label = tk.Label(root,text="Librabry management",font=("Aerial",20))
label.pack(padx=20,pady=20)
#Books ----------------------------------------
book_frame = tk.LabelFrame(root, text="Book Management",font=("Aerial",15))
book_frame.pack(fill="both", expand="yes", padx=10, pady=10)

tk.Label(book_frame, text="Book ID:",font=("Aerial",10)).grid(row=0, column=0, padx=5, pady=5)
book_id_entry = tk.Entry(book_frame)
book_id_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(book_frame, text="Book Name:",font=("Aerial",10)).grid(row=1, column=0, padx=5, pady=5)
book_name_entry = tk.Entry(book_frame)
book_name_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(book_frame, text="Quantity:",font=("Aerial",10)).grid(row=2, column=0, padx=5, pady=5)
quantity_entry = tk.Entry(book_frame)
quantity_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(book_frame, text="Field:",font=("Aerial",10)).grid(row=3, column=0, padx=5, pady=5)
field_entry = tk.Entry(book_frame)
field_entry.grid(row=3, column=1, padx=5, pady=5)

# Options ----------------------------------------------------------------
tk.Button(book_frame, text="Add Book", command=add_book).grid(row=4, column=0, padx=5, pady=5)
tk.Button(book_frame, text="Search Book", command=search_book).grid(row=4, column=1, padx=5, pady=5)
tk.Button(book_frame, text="Delete Book", command=delete_book).grid(row=4, column=2, padx=5, pady=5)
tk.Button(book_frame,text="Display all books",command=display_books).grid(row=4, column=3, padx=5, pady=5)

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

root.mainloop()