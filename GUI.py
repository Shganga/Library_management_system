import tkinter as tk
from functools import partial
from tkinter import messagebox
import pandas as pd
from werkzeug.security import check_password_hash
from Menagment.librarians import Librarians
from Menagment.books.bookFactory import BookFactory

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Library System")
        self.root.geometry("400x400")
        self.session = None

        self.user_bar = tk.Frame(self.root, height=40, bg="#000000")
        self.user_bar.pack(side="top", fill="x")
        self.login_button = tk.Button(self.user_bar, text="Login", command=self.show_login_page)
        self.register_button = tk.Button(self.user_bar, text="Register", command=self.show_register_page)
        self.logout_button = tk.Button(self.user_bar, text="Logout", command=self.logout)
        # Start the application
        self.refresh_page()
        self.show_start_page()


    def refresh_page(self):
        if self.session is None:
            self.login_button.pack(pady=10, side="right", padx=5 )
            self.register_button.pack(pady=10,side="right", padx=5)
            self.logout_button.pack_forget()
        else:
            self.logout_button.pack(pady=10,side="right", padx=5)
            self.login_button.pack_forget()
            self.register_button.pack_forget()


    def clear_window(self):
        for widget in self.root.winfo_children():
            if widget != self.user_bar:
                widget.destroy()

    def logout(self):
        self.session = None  # Clear the session
        self.refresh_page()


    def show_start_page(self):

        self.refresh_page()
        label = tk.Label(self.root, text="Library Management", font=("Arial", 16))
        label.pack(pady=20)

        # Add Book Button
        add_book_button = tk.Button(self.root, text="Add book page", command=lambda: self.check_session_and_execute(self.show_add_book))
        add_book_button.pack(pady=10)

        # Remove Book Button
        remove_book_button = tk.Button(self.root, text="Remove Book", command=lambda: self.check_session_and_execute(self.remove_book))
        remove_book_button.pack(pady=10)

        # Search Book Button
        search_book_button = tk.Button(self.root, text="Search Book", command=lambda: self.check_session_and_execute(self.search_book))
        search_book_button.pack(pady=10)

        # View Books Button
        view_books_button = tk.Button(self.root, text="View Books", command=lambda: self.check_session_and_execute(self.view_books))
        view_books_button.pack(pady=10)

        # Lend Book Button
        lend_book_button = tk.Button(self.root, text="Lend Book", command=lambda: self.check_session_and_execute(self.lend_book))
        lend_book_button.pack(pady=10)

        # Return Book Button
        return_book_button = tk.Button(self.root, text="Return Book", command=lambda: self.check_session_and_execute(self.return_book))
        return_book_button.pack(pady=10)

        # Popular Books Button
        popular_books_button = tk.Button(self.root, text="Popular Books", command=lambda: self.check_session_and_execute(self.popular_books))
        popular_books_button.pack(pady=10)
        # if self.session:
        #     label = tk.Label(self.root, text=f"Welcome {self.session['librarian']}!", font=("Arial", 16))
        #     label.pack(pady=20)
        #
        #     logout_button = tk.Button(self.root, text="Logout", command=self.logout)
        #     logout_button.pack(pady=10)
        # else:
        #     label = tk.Label(self.root, text="Welcome to the Library System", font=("Arial", 16))
        #     label.pack(pady=20)
        #
        #     login_button = tk.Button(self.root, text="Login", command=self.show_login_page)
        #     login_button.pack(pady=10)
        #
        #     register_button = tk.Button(self.root, text="Register", command=self.show_register_page)
        #     register_button.pack(pady=10)

    def show_login_page(self):
        self.clear_window()
        label = tk.Label(self.root, text="Login", font=("Arial", 16))
        label.pack(pady=20)

        username_label = tk.Label(self.root, text="Username:")
        username_label.pack(pady=5)
        username_entry = tk.Entry(self.root)
        username_entry.pack(pady=5)

        password_label = tk.Label(self.root, text="Password:")
        password_label.pack(pady=5)
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack(pady=5)

        login_button = tk.Button(self.root, text="Login",
                                 command=lambda: self.login(username_entry.get(), password_entry.get()))
        login_button.pack(pady=10)





    def login(self, username, password):
        users_csv = pd.read_csv("users.csv")
        user_row = users_csv[users_csv["username"] == username]
        if not user_row.empty:
            if check_password_hash(str(user_row["password"].values[0]), password):
                librarian = Librarians(username, password)
                self.session = {'librarian': librarian}
                messagebox.showinfo("Login", "Login Successful!")
                self.clear_window()
                self.show_start_page()
            else:
                self.session = None
                messagebox.showerror("Login", "Invalid password!")
        else:
            messagebox.showerror("Login", "Invalid username!")
        self.refresh_page()

    def show_register_page(self):
        self.clear_window()

        label = tk.Label(self.root, text="Register", font=("Arial", 16))
        label.pack(pady=20)

        username_label = tk.Label(self.root, text="Username:")
        username_label.pack(pady=5)
        username_entry = tk.Entry(self.root)
        username_entry.pack(pady=5)

        password_label = tk.Label(self.root, text="Password:")
        password_label.pack(pady=5)
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack(pady=5)

        confirm_password_label = tk.Label(self.root, text="Confirm Password:")
        confirm_password_label.pack(pady=5)
        confirm_password_entry = tk.Entry(self.root, show="*")
        confirm_password_entry.pack(pady=5)

        register_button = tk.Button(self.root, text="Register", command=lambda: self.register(username_entry.get(), password_entry.get(), confirm_password_entry.get()))
        register_button.pack(pady=10)


    def register(self, username, password, confirm_password):
        users_csv = pd.read_csv("users.csv")
        if username not in users_csv["username"]:
            if password == confirm_password:
                librarian = Librarians(username, password)

                new_user = {"username": librarian.get_username(), "password": librarian.get_password()}
                users_csv = users_csv._append(new_user, ignore_index=True)
                users_csv.to_csv("users.csv", index=False)

                self.session = {'librarian': librarian}

                messagebox.showinfo("Register", f"User '{username}' has been registered successfully!")
                self.show_start_page()
            else:
                self.session = None
                messagebox.showerror("Register", "Passwords do not match!")
        else:
            messagebox.showerror("Register", "Username already registered!")
        self.refresh_page()

    def show_add_book(self):
        self.clear_window()

        # Create the login page widgets
        label = tk.Label(self.root, text="add book", font=("Arial", 16))
        label.pack(pady=20)

        title_label = tk.Label(self.root, text="title:")
        title_label.pack(pady=5)
        title_entry = tk.Entry(self.root)
        title_entry.pack(pady=5)

        year_label = tk.Label(self.root, text="year:")
        year_label.pack(pady=5)
        year_entry = tk.Entry(self.root)
        year_entry.pack(pady=5)

        author_label = tk.Label(self.root, text="author:")
        author_label.pack(pady=5)
        author_entry = tk.Entry(self.root)
        author_entry.pack(pady=5)

        genre_label = tk.Label(self.root, text="genre:")
        genre_label.pack(pady=5)
        genre_entry = tk.Entry(self.root)
        genre_entry.pack(pady=5)

        copy_label = tk.Label(self.root, text="copy:")
        copy_label.pack(pady=5)
        copy_entry = tk.Entry(self.root)
        copy_entry.pack(pady=5)

        submit_button = tk.Button(self.root, text="add",
                                  command=partial(self.add_book, title_entry.get(), year_entry.get(), author_entry.get(),
                                                  genre_entry.get(), copy_entry.get()))
        submit_button.pack(pady=10)

        return_button = tk.Button(self.root, text="back", command=self.show_start_page)
        return_button.pack(pady=10)


    # Placeholder functions for the book actions
    def add_book(self,title, author, copies, genre, year):
        book = BookFactory.create_book(title, author, copies, genre, year)
        self.session['librarian'].add_book(book)
        messagebox.showinfo("Add Book", "Add Book functionality")

    def show_remove_book(self):
        self.clear_window()
        label = tk.Label(self.root, text="remove book", font=("Arial", 16))
        label.pack(pady=20)

        title_label = tk.Label(self.root, text="title:")
        title_label.pack(pady=5)
        title_entry = tk.Entry(self.root)
        title_entry.pack(pady=5)

        author_label = tk.Label(self.root, text="author:")
        author_label.pack(pady=5)
        author_entry = tk.Entry(self.root)
        author_entry.pack(pady=5)

        delete_button = tk.Button(self.root, text="delete",command=partial(self.remove_book, title_entry.get(), author_entry.get()))
        delete_button.pack(pady=10)

        return_button = tk.Button(self.root, text="back", command=self.show_start_page)
        return_button.pack(pady=10)

    def remove_book(self,title, author):
        ####
        messagebox.showinfo("Remove Book", "Remove Book functionality")

    def search_book(self):
        messagebox.showinfo("Search Book", "Search Book functionality")

    def view_books(self):
        messagebox.showinfo("View Books", "View Books functionality")

    def show_lend_book(self):
        self.clear_window()
        label = tk.Label(self.root, text="lend book")
        label.pack(pady=20)

        title_label = tk.Label(self.root, text="title:")
        title_label.pack(pady=5)
        title_entry = tk.Entry(self.root)
        title_entry.pack(pady=5)

        author_label = tk.Label(self.root, text="author:")
        author_label.pack(pady=5)
        author_entry = tk.Entry(self.root)
        author_entry.pack(pady=5)

        phone_label = tk.Label(self.root, text="phone:")
        phone_label.pack(pady=5)
        phone_entry = tk.Entry(self.root)
        phone_entry.pack(pady=5)

        lend_book_button = tk.Button(self.root, text="Lend Book",command=partial(self.lend_book, title_entry.get(), author_entry.get(),phone_entry.get()))
        lend_book_button.pack(pady=10)

        return_button = tk.Button(self.root, text="back", command=self.show_start_page)
        return_button.pack(pady=10)

    def lend_book(self,title, author, phone_number):
        self.session['librarian'].borrow_book(title, author, phone_number)
        messagebox.showinfo("Lend Book", "Lend Book functionality")

    def show_return_book(self):
        self.clear_window()
        label = tk.Label(self.root, text="remove book", font=("Arial", 16))
        label.pack(pady=20)

        title_label = tk.Label(self.root, text="title:")
        title_label.pack(pady=5)
        title_entry = tk.Entry(self.root)
        title_entry.pack(pady=5)

        author_label = tk.Label(self.root, text="author:")
        author_label.pack(pady=5)
        author_entry = tk.Entry(self.root)
        author_entry.pack(pady=5)

        phone_label = tk.Label(self.root, text="phone:")
        phone_label.pack(pady=5)
        phone_entry = tk.Entry(self.root)
        phone_entry.pack(pady=5)

        return_button = tk.Button(self.root, text="return",
                                  command=partial(self.return_book, title_entry.get(), author_entry.get(),
                                                  phone_entry.get()))
        return_button.pack(pady=10)

        return_button = tk.Button(self.root, text="back", command= self.show_start_page)
        return_button.pack(pady=10)

    def return_book(self,title, author, phone_number):
        self.session['librarian'].return_book(title, author, phone_number)
        messagebox.showinfo("Return Book", "Return Book functionality")

    def popular_books(self):
        messagebox.showinfo("Popular Books", "Popular Books functionality")

    def check_session_and_execute(self, func):
        def wrapper(*args, **kwargs):
            if self.session is None:
                messagebox.showerror("Error", "Session not active. Please log in first.")
            else:
                return func(*args, **kwargs)

        return wrapper


