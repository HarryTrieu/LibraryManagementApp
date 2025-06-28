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

label = tk.Label(root,text="Librabry management",font=("Aerial",20))
label.pack(padx=20,pady=20)
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
    new_window.geometry("900x700")

    with open('books.json', 'r') as f:
        books_data = json.load(f)

    if books_data:
        all_books = tk.Text(new_window)
        all_books.pack(fill="both", expand=True)
        all_books.insert(tk.END, "All Books:\n" + "\n".join(f"{book['name']} ({book_id})" for book_id, book in books_data.items()))
    else:
        tk.Label(new_window, text="No books available.").pack(padx=10, pady=10)


# Borrowing and Returning Management Functions
def borrow_book():
    book_id = book_id_entry.get()
    if book_id in books and books[book_id]['status'] == "Available":
        student_id = student_id_entry.get()
        due_date = datetime.datetime.now() + datetime.timedelta(days=7)  # Due date set to 7 days from now
        borrowed_books[book_id] = {"student_id": student_id, "due_date": due_date.strftime("%Y-%m-%d")}
        books[book_id]['status'] = "Borrowed"
        save_data()
        messagebox.showinfo("Success", f"Book '{books[book_id]['name']}' borrowed by student '{student_id}'. Due Date: {due_date.strftime('%Y-%m-%d')}")
    else:
        messagebox.showwarning("Unavailable", "Book not exist or already borrowed.")
    clear_borrow_entries()

def return_book():
    book_id = borrow_book_id_entry.get()
    if book_id in borrowed_books:
        book_name = books[book_id]['name']
        return_date = datetime.datetime.now().strftime("%Y-%m-%d")  # Get the current date as the return date
        del borrowed_books[book_id]
        books[book_id]['status'] = "Available"
        returned_books[book_id] = return_date  # Add the book ID and return date to returned_books
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
    new_window = tk.Toplevel(root)
    new_window.title("Returned Books")
    new_window.geometry("400x300")

    if returned_books:
        returned_books_text = tk.Text(new_window)
        returned_books_text.pack(fill="both", expand=True)

        for book_id, return_date in returned_books.items():
            if book_id in books:
                book_name = books[book_id]["name"]
                returned_books_text.insert(tk.END, f"{book_name} ({book_id}) returned on {return_date}\n")
            else:
                returned_books_text.insert(tk.END, f"Unknown Book ({book_id}) returned on {return_date}\n")
    else:
        tk.Label(new_window, text="No returned books.").pack(padx=10, pady=10)


# Seat Management Functions
def add_seats():
    row = seat_row_entry.get()
    num_seats = int(num_seats_entry.get())
    if row not in seats:
        seats[row] = [True] * num_seats  
        save_data()
        messagebox.showinfo("Success", f"Added {num_seats} seats in row '{row}'")
    else:
        messagebox.showwarning("Error", f"Row '{row}' already exists. Cannot add seats.")
    clear_seat_entries()

def find_empty_seat():
    row = seat_row_entry.get()
    if row in seats:
        empty_seats = [f"SEAT{i+1}" for i, is_available in enumerate(seats[row]) if is_available]
        if empty_seats:
            messagebox.showinfo("Empty Seats", f"Empty seats in row '{row}': {', '.join(empty_seats)}")
        else:
            messagebox.showinfo("No Empty Seats", f"No empty seats in row '{row}'.")
    else:
        messagebox.showwarning("Error", "Row not found.")
    clear_seat_entries()



def occupy_seat():
    row = seat_row_entry2.get()
    seat_number = int(seat_number_entry.get())
    if row in seats and 1 <= seat_number <= len(seats[row]):
        if seats[row][seat_number - 1]:
            seats[row][seat_number - 1] = False  # Mark seat as occupied
            save_data()
            messagebox.showinfo("Success", f"Seat {row}-{seat_number} is now occupied.")
        else:
            messagebox.showwarning("Occupied Seat", f"Seat {row}-{seat_number} is already occupied.")
    else:
        messagebox.showwarning("Invalid Seat", "Invalid row or seat number.")
    clear_seat_entries()

def clear_seat():
    row = seat_row_entry2.get()
    seat_number = int(seat_number_entry.get())
    if row in seats and 1 <= seat_number <= len(seats[row]):
        if not seats[row][seat_number - 1]:
            seats[row][seat_number - 1] = True  # Mark seat as available
            save_data()
            messagebox.showinfo("Success", f"Seat {row}-{seat_number} is now available.")
        else:
            messagebox.showwarning("Empty Seat", f"Seat {row}-{seat_number} is already available.")
    else:
        messagebox.showwarning("Invalid Seat", "Invalid row or seat number.")
    clear_seat_entries()



def clear_seat_entries():
    seat_row_entry.delete(0, tk.END)
    num_seats_entry.delete(0, tk.END)
    seat_number_entry.delete(0, tk.END)

# Adding a new student
def add_student():
    student_id = student_id_entry.get()
    student_name = student_name_entry.get()
    students[student_id] = student_name
    save_data()
    messagebox.showinfo("Success", f"Student '{student_name}' added successfully with ID: {student_id}")
    clear_student_entries()

def clear_student_entries():
    student_id_entry.delete(0, tk.END)
    student_name_entry.delete(0, tk.END)
    
def display_all_students():
    new_window = Toplevel(root)
    new_window.title("All Students")
    new_window.geometry("900x700")
    try:
        with open(STUDENTS_FILE, 'r') as f:
            student_data = json.load(f)
    except FileNotFoundError:
        tk.Label(new_window, text="Student data file not found.").pack(padx=10, pady=10)
        return
    except json.JSONDecodeError:
        tk.Label(new_window, text="Error decoding student data.").pack(padx=10, pady=10)
        return

    print("Student data received in display function:", student_data) 

    if student_data:
        all_students = tk.Text(new_window)
        all_students.pack(fill="both", expand=True)
        all_students.insert(tk.END, "All Students:\n" + "\n".join(f"ID: {student_id}, Name: {student_name}" for student_id, student_name in student_data.items()))
    else:
        tk.Label(new_window, text="No students available.").pack(padx=10, pady=10)



# Book Management GUI
book_frame = tk.LabelFrame(root, text="Book Management")
book_frame.pack(fill="both", expand="yes", padx=10, pady=10)

tk.Label(book_frame, text="Book ID:").grid(row=0, column=0, padx=5, pady=5)
book_id_entry = tk.Entry(book_frame)
book_id_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(book_frame, text="Book Name:").grid(row=1, column=0, padx=5, pady=5)
book_name_entry = tk.Entry(book_frame)
book_name_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(book_frame, text="Field:").grid(row=2, column=0, padx=5, pady=5)
field_entry = tk.Entry(book_frame)
field_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Button(book_frame, text="Add Book", command=add_book).grid(row=3, column=0, padx=5, pady=5)
tk.Button(book_frame, text="Search Book", command=search_book).grid(row=3, column=1, padx=5, pady=5)
tk.Button(book_frame, text="Delete Book", command=delete_book).grid(row=3, column=2, padx=5, pady=5)
tk.Button(book_frame, text="Display All Books", command=display_all_books).grid(row=3, column=3, padx=5, pady=5)

# Borrowing and Returning Management GUI
debt_frame = tk.LabelFrame(root, text="Borrowing and Returning Management")
debt_frame.pack(fill="both", expand="yes", padx=10, pady=10)

tk.Label(debt_frame, text="Student ID:").grid(row=0, column=0, padx=5, pady=5)
student_id_entry = tk.Entry(debt_frame)
student_id_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(debt_frame, text="Book ID:").grid(row=1, column=0, padx=5, pady=5)
borrow_book_id_entry = tk.Entry(debt_frame)
borrow_book_id_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Button(debt_frame, text="Borrow Book", command=borrow_book).grid(row=2, column=0, padx=5, pady=5)
tk.Button(debt_frame, text="Return Book", command=return_book).grid(row=2, column=1, padx=5, pady=5)
tk.Button(debt_frame, text="Display Borrowed Books", command=display_borrowed_books).grid(row=3, column=0, padx=5, pady=5)
tk.Button(debt_frame, text="Display Returned Books", command=display_returned_books).grid(row=3, column=1, padx=5, pady=5)

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

tk.Label(seat_frame, text="Seat Row:").grid(row=4, column=0, padx=5, pady=5)
seat_row_entry2 = tk.Entry(seat_frame)
seat_row_entry2.grid(row=4, column=1, padx=5, pady=5)  

tk.Label(seat_frame, text="Seat Number:").grid(row=5, column=0, padx=5, pady=5)  
seat_number_entry = tk.Entry(seat_frame)
seat_number_entry.grid(row=5, column=1, padx=5, pady=5) 

tk.Button(seat_frame, text="Occupy Seat", command=occupy_seat).grid(row=6, column=0, padx=5, pady=5)
tk.Button(seat_frame, text="Clear Seat", command=clear_seat).grid(row=6, column=1, padx=5, pady=5)

# Student Management GUI
student_frame = tk.LabelFrame(root, text="Student Management")
student_frame.pack(fill="both", expand="yes", padx=10, pady=10)

tk.Label(student_frame, text="Student ID:").grid(row=0, column=0, padx=5, pady=5)
student_id_entry = tk.Entry(student_frame)
student_id_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(student_frame, text="Student Name:").grid(row=1, column=0, padx=5, pady=5)
student_name_entry = tk.Entry(student_frame)
student_name_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Button(student_frame, text="Add Student", command=add_student).grid(row=2, column=0, columnspan=2, padx=5, pady=5)


display_all_students_button = tk.Button(student_frame, text="Display All Students", command=display_all_students)
display_all_students_button.grid(row=2, column=2,padx=3, pady=3)



root.mainloop()
