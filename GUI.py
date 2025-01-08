import tkinter as tk
from functools import partial
from tkinter import messagebox
import pandas as pd
from werkzeug.security import check_password_hash
from Menagment.librarians import Librarians
from Menagment.books.bookFactory import  BookFactory

# Function to show the login page
def show_login_page():
    clear_window()

    # Create the login page widgets
    label = tk.Label(root, text="Login", font=("Arial", 16))
    label.pack(pady=20)

    username_label = tk.Label(root, text="Username:")
    username_label.pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    password_label = tk.Label(root, text="Password:")
    password_label.pack(pady=5)
    password_entry = tk.Entry(root, show="*")  # Hide password
    password_entry.pack(pady=5)

    login_button = tk.Button(root, text="Login", command=lambda: login(username_entry.get(), password_entry.get()))
    login_button.pack(pady=10)

    register_button = tk.Button(root, text="Register", command=show_register_page)
    register_button.pack(pady=10)


# Function to handle login
def login(username, password):
    global session
    users_csv = pd.read_csv("users.csv")
    user_row = users_csv[users_csv["username"] == username]
    if not user_row.empty:
        if check_password_hash(str(user_row["password"].values[0]), password):
            librarian = Librarians(username, password)
            session = {'librarian': librarian}
            messagebox.showinfo("Login", "Login Successful!")
            show_book_management_page()
        else:
            session = None
            messagebox.showerror("Login", "Invalid password!")
    else:
        messagebox.showerror("Login", "Invalid username!")


# Function to show the register page
def show_register_page():
    clear_window()

    # Create the register page widgets
    label = tk.Label(root, text="Register", font=("Arial", 16))
    label.pack(pady=20)

    username_label = tk.Label(root, text="Username:")
    username_label.pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    password_label = tk.Label(root, text="Password:")
    password_label.pack(pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    confirm_password_label = tk.Label(root, text="Confirm Password:")
    confirm_password_label.pack(pady=5)
    confirm_password_entry = tk.Entry(root, show="*")
    confirm_password_entry.pack(pady=5)

    register_button = tk.Button(root, text="Register",
                                command=lambda: register(username_entry.get(), password_entry.get(),
                                                         confirm_password_entry.get()))
    register_button.pack(pady=10)

    login_button = tk.Button(root, text="login", command=show_login_page)
    login_button.pack(pady=10)


# Function to handle registration
def register(username, password, confirm_password):
    users_csv = pd.read_csv("users.csv")
    if username not in users_csv["username"]:
        if password == confirm_password:
            librarian = Librarians(username, password)

            new_user = {"username": librarian.get_username(), "password": librarian.get_password()}
            users_csv = users_csv._append(new_user, ignore_index=True)
            users_csv.to_csv("users.csv", index=False)

            session = {'librarian': librarian}

            messagebox.showinfo("Register", f"User '{username}' has been registered successfully!")
            show_start_page()  # Go back to start page after registration
        else:
            session = None
            messagebox.showerror("Register", "Passwords do not match!")
    else:
        messagebox.showerror("Register", "Username already registered!")


# Function to clear the window (remove all widgets)
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


# Function to log out (clear the session)
def logout():
    global session
    session = None  # Clear the session
    show_start_page()


# Display the starter page with options to log in or register
def show_start_page():
    clear_window()

    if session:
        label = tk.Label(root, text=f"Welcome {session['librarian']}!", font=("Arial", 16))
        label.pack(pady=20)

        logout_button = tk.Button(root, text="Logout", command=logout)
        logout_button.pack(pady=10)
    else:
        label = tk.Label(root, text="Welcome to the Library System", font=("Arial", 16))
        label.pack(pady=20)

        login_button = tk.Button(root, text="Login", command=show_login_page)
        login_button.pack(pady=10)

        register_button = tk.Button(root, text="Register", command=show_register_page)
        register_button.pack(pady=10)


# Function to show the Book Management Page
def show_book_management_page():
    clear_window()

    label = tk.Label(root, text="Library Management", font=("Arial", 16))
    label.pack(pady=20)

    # Add Book Button
    add_book_button = tk.Button(root, text="Add book page", command=lambda: show_add_book())
    add_book_button.pack(pady=10)

    # Remove Book Button
    remove_book_button = tk.Button(root, text="Remove Book", command=lambda: remove_book)
    remove_book_button.pack(pady=10)

    # Search Book Button
    search_book_button = tk.Button(root, text="Search Book", command=search_book)
    search_book_button.pack(pady=10)

    # View Books Button
    view_books_button = tk.Button(root, text="View Books", command=view_books)
    view_books_button.pack(pady=10)

    # Lend Book Button
    lend_book_button = tk.Button(root, text="Lend Book", command=lend_book)
    lend_book_button.pack(pady=10)

    # Return Book Button
    return_book_button = tk.Button(root, text="Return Book", command=return_book)
    return_book_button.pack(pady=10)

    # Popular Books Button
    popular_books_button = tk.Button(root, text="Popular Books", command=popular_books)
    popular_books_button.pack(pady=10)

    # Logout Button
    logout_button = tk.Button(root, text="Logout", command=logout)
    logout_button.pack(pady=10)

def show_add_book():
    clear_window()

    # Create the login page widgets
    label = tk.Label(root, text="add book", font=("Arial", 16))
    label.pack(pady=20)

    title_label = tk.Label(root, text="title:")
    title_label.pack(pady=5)
    title_entry = tk.Entry(root)
    title_entry.pack(pady=5)

    year_label = tk.Label(root, text="year:")
    year_label.pack(pady=5)
    year_entry = tk.Entry(root)
    year_entry.pack(pady=5)

    author_label = tk.Label(root, text="author:")
    author_label.pack(pady=5)
    author_entry = tk.Entry(root)
    author_entry.pack(pady=5)

    genre_label = tk.Label(root, text="genre:")
    genre_label.pack(pady=5)
    genre_entry = tk.Entry(root)
    genre_entry.pack(pady=5)

    copy_label = tk.Label(root, text="copy:")
    copy_label.pack(pady=5)
    copy_entry = tk.Entry(root)
    copy_entry.pack(pady=5)

    submit_button = tk.Button(root, text="add", command=partial(add_book,title_entry.get(), year_entry.get(), author_entry.get(), genre_entry.get(),copy_entry.get()))
    submit_button.pack(pady=10)

    return_button = tk.Button(root, text="back", command=show_book_management_page)
    return_button.pack(pady=10)

def check_valid_year(year):
    return year <= 2025
# Placeholder functions for the book actions
def add_book(title, author, copies, genre, year):
    if session['librarian'] is None:
        show_book_management_page()
    book = BookFactory.create_book(title, author, copies, genre, year)
    session['librarian'].add_book(book)
    messagebox.showinfo("Add Book", "Add Book functionality")

def show_remove_book():
    clear_window()
    label = tk.Label(root, text="remove book", font=("Arial", 16))
    label.pack(pady=20)

    title_label = tk.Label(root, text="title:")
    title_label.pack(pady=5)
    title_entry = tk.Entry(root)
    title_entry.pack(pady=5)

    author_label = tk.Label(root, text="author:")
    author_label.pack(pady=5)
    author_entry = tk.Entry(root)
    author_entry.pack(pady=5)

    delete_button = tk.Button(root, text="delete", command= partial(remove_book,title_entry.get(), author_entry.get()))
    delete_button.pack(pady=10)

    return_button = tk.Button(root, text="back", command=show_book_management_page)
    return_button.pack(pady=10)


def remove_book(title, author):
    ####
    messagebox.showinfo("Remove Book", "Remove Book functionality")


def search_book():
    messagebox.showinfo("Search Book", "Search Book functionality")


def view_books():
    messagebox.showinfo("View Books", "View Books functionality")

def show_lend_book():
    clear_window()
    label = tk.Label(root, text="lend book")
    label.pack(pady=20)

    title_label = tk.Label(root, text="title:")
    title_label.pack(pady=5)
    title_entry = tk.Entry(root)
    title_entry.pack(pady=5)

    author_label = tk.Label(root, text="author:")
    author_label.pack(pady=5)
    author_entry = tk.Entry(root)
    author_entry.pack(pady=5)

    phone_label = tk.Label(root, text="phone:")
    phone_label.pack(pady=5)
    phone_entry = tk.Entry(root)
    phone_entry.pack(pady=5)

    lend_book_button = tk.Button(root, text="Lend Book", command=partial(lend_book,title_entry.get(), author_entry.get(), phone_entry.get()))
    lend_book_button.pack(pady=10)

    return_button = tk.Button(root, text="back", command=show_book_management_page)
    return_button.pack(pady=10)


def lend_book(title,author,phone_number):
    session['librarian'].borrow_book(title, author,phone_number)
    messagebox.showinfo("Lend Book", "Lend Book functionality")

def show_return_book():
    clear_window()
    label = tk.Label(root, text="remove book", font=("Arial", 16))
    label.pack(pady=20)

    title_label = tk.Label(root, text="title:")
    title_label.pack(pady=5)
    title_entry = tk.Entry(root)
    title_entry.pack(pady=5)

    author_label = tk.Label(root, text="author:")
    author_label.pack(pady=5)
    author_entry = tk.Entry(root)
    author_entry.pack(pady=5)

    phone_label = tk.Label(root, text="phone:")
    phone_label.pack(pady=5)
    phone_entry = tk.Entry(root)
    phone_entry.pack(pady=5)

    return_button = tk.Button(root, text="return", command=partial(return_book,title_entry.get(), author_entry.get(),phone_entry.get()))
    return_button.pack(pady=10)

    return_button = tk.Button(root, text="back", command=show_book_management_page)
    return_button.pack(pady=10)

def return_book(title, author,phone_number):
    session['librarian'].return_book(title, author, phone_number)
    messagebox.showinfo("Return Book", "Return Book functionality")


def popular_books():
    messagebox.showinfo("Popular Books", "Popular Books functionality")



if __name__ == '__main__':
    root = tk.Tk()
    root.title("Library System")
    root.geometry("400x400")

    session = None

    show_start_page()
    root.mainloop()



