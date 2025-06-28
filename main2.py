import tkinter as tk
from tkinter import messagebox, Toplevel
import json
import datetime

# File paths for storing data
BOOKS_FILE = 'books.json'
BORROWED_BOOKS_FILE = 'borrowed_books.json'
RETURNED_BOOKS_FILE = 'returned_books.json'
SEATS_FILE = 'seats.json'
STUDENTS_FILE = 'students.json'

root = tk.Tk()
root.title("Library Management System")
root.geometry("1000x800")

label = tk.Label(root, text="Library Management", font=("Arial", 20))
label.pack(padx=20, pady=20)

# These functions are for cleaning after actions
def clear_book_entries():
    book_id_entry.delete(0, tk.END)
    book_name_entry.delete(0, tk.END)
    field_entry.delete(0, tk.END)
    
def clear_borrow_entries():
    student_id_entry.delete(0, tk.END)
    borrow_book_id_entry.delete(0, tk.END)
    
def clear_return_entries():
    student_id_entry.delete(0, tk.END)
    borrow_book_id_entry.delete(0, tk.END)

# Load data function
def load_data():
    global books, borrowed_books, returned_books, seats, students
    with open(BOOKS_FILE, 'r') as f:
        books = json.load(f)
    with open(BORROWED_BOOKS_FILE, 'r') as f:
        borrowed_books = json.load(f)
    with open(RETURNED_BOOKS_FILE, 'r') as f:
        returned_books = json.load(f)
    with open(SEATS_FILE, 'r') as f:
        seats = json.load(f)
    with open(STUDENTS_FILE, 'r') as f:
        students = json.load(f)

# Save data function
def save_data():
    with open(BOOKS_FILE, 'w') as f:
        json.dump(books, f, indent=4)
    with open(BORROWED_BOOKS_FILE, 'w') as f:
        json.dump(borrowed_books, f, indent=4)
    with open(RETURNED_BOOKS_FILE, 'w') as f:
        json.dump(returned_books, f, indent=4)
    with open(SEATS_FILE, 'w') as f:
        json.dump(seats, f, indent=4)
    with open(STUDENTS_FILE, 'w') as f:
        json.dump(students, f, indent=4)

books = {}
borrowed_books = {}
returned_books = {}
seats = {}
students = {}

load_data()

# Book Management Functions
def add_book():
    book_id = book_id_entry.get().strip()
    book_name = book_name_entry.get().strip().lower()  # Convert to lowercase for case-insensitive search
    field = field_entry.get().strip()

    if book_id or book_name:  # Check if either book ID or name is provided
        status = "Available"  # New books are available by default
        if book_id != "":
            books[book_id] = {"name": book_name, "field": field, "status": status}
            save_data()  # Save the updated data to the JSON file
            messagebox.showinfo("Success", f"Book '{book_name}' added successfully.")
            clear_book_entries()
        else:
            messagebox.showwarning("Missing Information", "Please enter a book ID.")
    else:
        messagebox.showwarning("Missing Information", "Please type in the book name or ID to add the book.")

def search_book():
    # use strip to delete the white space
    search_id = book_id_entry.get().strip()
    search_name = book_name_entry.get().strip().lower()

    if search_id and not search_name:  # if only ID is provided
        if search_id in books:
            book = books[search_id]
            messagebox.showinfo("Book Found", f"Book ID: {search_id}\nBook Name: {book['name']}\nField: {book['field']}\nStatus: {book['status']}")
        else:
            messagebox.showwarning("Not Found", "Book ID not found.")
    elif not search_id and search_name:  # if only name is provided
        found_books = [(book_id, book) for book_id, book in books.items() if search_name in book['name'].lower()]
        if found_books:
            messagebox.showinfo("Books Found", "Found Books:\n" + "\n".join(f"{book[1]['name']} ({book[0]})" for book in found_books))
        else:
            messagebox.showwarning("Not Found", "No books found.")
    elif search_id and search_name:  # If both ID and name are provided
        if search_id in books:
            book = books[search_id]
            messagebox.showinfo("Book Found", f"Book ID: {search_id}\nBook Name: {book['name']}\nField: {book['field']}\nStatus: {book['status']}")
        else:
            found_books = [(book_id, book) for book_id, book in books.items() if search_name in book['name'].lower()]
            if found_books:
                messagebox.showinfo("Books Found", "Found Books:\n" + "\n".join(f"{book[1]['name']} ({book[0]})" for book in found_books))
            else:
                messagebox.showwarning("Not Found", "No books found with the provided ID or name.")
    else:
        messagebox.showwarning("Invalid Input", "Please provide either a Book ID or a Book Name.")

def delete_book():
    book_id = book_id_entry.get().strip()  # Retrieve the book ID entered by the user
    book_name = book_name_entry.get().strip().lower()  # Retrieve the book name entered by the user

    if book_id and not book_name:  # If only ID is provided
        if book_id in books:
            book_name = books[book_id]["name"]
            del books[book_id]
            save_data()
            messagebox.showinfo("Success", f"Book '{book_name}' deleted successfully.")
        else:
            messagebox.showwarning("Not Found", "Book ID not found.")
    elif not book_id and book_name:  # If only name is provided
        found_books = [book_id for book_id, book in books.items() if book['name'].lower() == book_name]
        if found_books:
            for book_id in found_books:
                del books[book_id]
            save_data()
            messagebox.showinfo("Success", f"Books with the name '{book_name}' deleted successfully.")
        else:
            messagebox.showwarning("Not Found", "No books found with the provided name.")
    elif book_id and book_name:  # If both ID and name are provided
        if book_id in books:
            book = books[book_id]
            if book['name'].lower() == book_name:
                del books[book_id]
                save_data()
                messagebox.showinfo("Success", f"Book '{book_name}' (ID: {book_id}) deleted successfully.")
            else:
                messagebox.showwarning("Mismatch", "Book ID and name do not match.")
        else:
            messagebox.showwarning("Not Found", "Book ID not found.")
    else:
        messagebox.showwarning("Invalid Input", "Please provide either a Book ID or a Book Name.")

    clear_book_entries()

def display_all_books():
    new_window = Toplevel(root)
    new_window.title("All Books")
    new_window.geometry("400x300")
    if books:
        all_books = tk.Text(new_window)
        all_books.pack(fill="both", expand=True)
        all_books.insert(tk.END, "All Books:\n" + "\n".join(f"{book['name']} ({book_id})" for book_id, book in books.items()))
    else:
        tk.Label(new_window, text="No books available.").pack(padx=10, pady=10)

# Borrowing and Returning Management Functions
def borrow_book():
    book_id = borrow_book_id_entry.get()
    if book_id in books and books[book_id]['status'] == "Available":
        student_id = student_id_entry.get()
        due_date = datetime.datetime.now() + datetime.timedelta(days=7)  # Due date set to 7 days from now
        borrowed_books[book_id] = {"student_id": student_id, "due_date": due_date.strftime("%Y-%m-%d")}
        books[book_id]['status'] = "Borrowed"
        save_data()
        messagebox.showinfo("Success", f"Book '{books[book_id]['name']}' borrowed by student '{student_id}'. Due Date: {due_date.strftime('%Y-%m-%d')}")
    else:
        messagebox.showwarning("Unavailable", "Book not available for borrowing or already borrowed.")
    clear_borrow_entries()

def return_book():
    book_id = borrow_book_id_entry.get()
    if book_id in borrowed_books:
        book_name = books[book_id]['name']
        del borrowed_books[book_id]
        books[book_id]['status'] = "Available"
        save_data()
        messagebox.showinfo("Success", f"Book '{book_name}' returned successfully.")
    else:
        messagebox.showwarning("Error", "Book not borrowed.")
    clear_return_entries()

def display_borrowed_books():
    new_window = Toplevel(root)
    new_window.title("Borrowed Books")
    new_window.geometry("400x300")
    if borrowed_books:
        borrowed_books_text = tk.Text(new_window)
        borrowed_books_text.pack(fill="both", expand=True)
        borrowed_books_text.insert(tk.END, "Borrowed Books:\n" + "\n".join(f"{books[book_id]['name']} ({book_id}) by Student ID: {details['student_id']} (Due: {details['due_date']})" for book_id, details in borrowed_books.items()))
    else:
        tk.Label(new_window, text="No borrowed books.").pack(padx=10, pady=10)

def display_returned_books():
    new_window = Toplevel(root)
    new_window.title("Returned Books")
    new_window.geometry("400x300")
    if returned_books:
        returned_books_text = tk.Text(new_window)
        returned_books_text.pack(fill="both", expand=True)
        returned_books_text.insert(tk.END, "Returned Books:\n" + "\n".join(f"{books[book_id]['name']} ({book_id}) returned on {return_date}" for book_id, return_date in returned_books.items()))
    else:
        tk.Label(new_window, text="No returned books.").pack(padx=10, pady=10)

# Student Management Functions
def display_all_students():
    new_window = Toplevel(root)
    new_window.title("All Students")
    new_window.geometry("400x300")
    if students:
        all_students = tk.Text(new_window)
        all_students.pack(fill="both", expand=True)
        all_students.insert(tk.END, "All Students:\n" + "\n".join(f"ID: {student_id}, Name: {student['name']}" for student_id, student in students.items()))
    else:
        tk.Label(new_window, text="No students available.").pack(padx=10, pady=10)

# GUI for Books
book_frame = tk.Frame(root)
book_frame.pack(padx=10, pady=10, fill="x")

book_id_label = tk.Label(book_frame, text="Book ID")
book_id_label.grid(row=0, column=0)
book_id_entry = tk.Entry(book_frame)
book_id_entry.grid(row=0, column=1)

book_name_label = tk.Label(book_frame, text="Book Name")
book_name_label.grid(row=1, column=0)
book_name_entry = tk.Entry(book_frame)
book_name_entry.grid(row=1, column=1)

field_label = tk.Label(book_frame, text="Field")
field_label.grid(row=2, column=0)
field_entry = tk.Entry(book_frame)
field_entry.grid(row=2, column=1)

add_book_button = tk.Button(book_frame, text="Add Book", command=add_book)
add_book_button.grid(row=3, column=0, pady=5)

search_book_button = tk.Button(book_frame, text="Search Book", command=search_book)
search_book_button.grid(row=3, column=1, pady=5)

delete_book_button = tk.Button(book_frame, text="Delete Book", command=delete_book)
delete_book_button.grid(row=3, column=2, pady=5)

display_all_books_button = tk.Button(book_frame, text="Display All Books", command=display_all_books)
display_all_books_button.grid(row=3, column=3, pady=5)

# GUI for Borrowing and Returning Books
borrow_frame = tk.Frame(root)
borrow_frame.pack(padx=10, pady=10, fill="x")

student_id_label = tk.Label(borrow_frame, text="Student ID")
student_id_label.grid(row=0, column=0)
student_id_entry = tk.Entry(borrow_frame)
student_id_entry.grid(row=0, column=1)

borrow_book_id_label = tk.Label(borrow_frame, text="Book ID")
borrow_book_id_label.grid(row=1, column=0)
borrow_book_id_entry = tk.Entry(borrow_frame)
borrow_book_id_entry.grid(row=1, column=1)

borrow_book_button = tk.Button(borrow_frame, text="Borrow Book", command=borrow_book)
borrow_book_button.grid(row=2, column=0, pady=5)

return_book_button = tk.Button(borrow_frame, text="Return Book", command=return_book)
return_book_button.grid(row=2, column=1, pady=5)

display_borrowed_books_button = tk.Button(borrow_frame, text="Display Borrowed Books", command=display_borrowed_books)
display_borrowed_books_button.grid(row=2, column=2, pady=5)

display_returned_books_button = tk.Button(borrow_frame, text="Display Returned Books", command=display_returned_books)
display_returned_books_button.grid(row=2, column=3, pady=5)

# GUI for Students
student_frame = tk.Frame(root)
student_frame.pack(padx=10, pady=10, fill="x")

display_all_students_button = tk.Button(student_frame, text="Display All Students", command=display_all_students)
display_all_students_button.grid(row=0, column=0, pady=5)

root.mainloop()

