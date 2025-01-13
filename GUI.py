import ast
import tkinter as tk
from functools import partial
from re import search
from tkinter import messagebox
from tkinter.constants import MULTIPLE, SINGLE
import logging

import pandas as pd
from werkzeug.security import check_password_hash
from Menagment.librarians import Librarians
from Menagment.books.bookFactory import BookFactory

class GUI:
    def __init__(self, root,logging):
        self.root = root
        self.root.title("Library System")
        self.root.geometry("1000x700")
        self.session = None
        self.search_strategy = None

        self.logging = logging

        self.user_bar = tk.Frame(self.root, height=40, bg="#000000")
        self.user_bar.pack(side="top", fill="x")
        self.login_button = tk.Button(self.user_bar, text="login", command=self.show_login_page)
        self.register_button = tk.Button(self.user_bar, text="Register", command=self.show_register_page)
        self.logout_button = tk.Button(self.user_bar, text="Logout", command=self.logout)
        self.notify_button = tk.Button(self.user_bar, text="💬", command=self.show_notifications)
        # Start the application
        self.refresh_page()
        self.show_start_page()


    def refresh_page(self):
        if self.session is None:
            self.login_button.pack(pady=10, side="right", padx=5 )
            self.register_button.pack(pady=10,side="right", padx=5)
            self.notify_button.pack_forget()
            self.logout_button.pack_forget()
        else:
            self.logout_button.pack(pady=10,side="right", padx=5)
            self.notify_button.pack(pady=10, side="right", padx=5)
            self.login_button.pack_forget()
            self.register_button.pack_forget()


    def clear_window(self):
        for widget in self.root.winfo_children():
            if widget != self.user_bar:
                widget.destroy()

    def logout(self):
        self.session = None
        messagebox.showinfo("logout", "logged out successfully")
        self.logging.info("log out successful")
        self.show_start_page()# Clear the session
        self.refresh_page()

    def show_notifications(self):
        self.clear_window()
        users_csv = pd.read_csv("users.csv")
        user_row = users_csv[users_csv["username"] == self.session['librarian'].get_username()]
        notifications = user_row["notification"].values[0]

        if isinstance(notifications, str):
            try:
                notifications = ast.literal_eval(notifications)  # Convert string to list if necessary
                if not isinstance(notifications, list):  # Check if it's actually a list after eval
                    notifications = []
            except:
                notifications = []  # Default to empty list if conversion fails
        elif not isinstance(notifications, list):
            notifications = []  # In case it's neither a string nor list, default to an empty list

        listbox = tk.Listbox(self.root, height=10, width=60)
        listbox.pack(pady=20)

        # Add a scrollbar for the listbox
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=listbox.yview)
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        delete_msg_button = tk.Button(self.root, text="delete", command=lambda: self.delete_notification(listbox))
        delete_msg_button.pack(side="center", padx=5, pady=5)

        # Insert each notification into the listbox
        for notification in notifications:
            listbox.insert(tk.END, notification)

        # Optional: you can add a message if there are no notifications
        if not notifications:
            listbox.insert(tk.END, "No notifications available.")
    def delete_notification(self, list_box):
        selected_index = list_box.curselection()
        did_work = self.session['librarian'].remove_notification(selected_index)
        if did_work:
            messagebox.showinfo("Notification was deleted")
        else:
            messagebox.showerror("something went wrong")
        self.show_notifications()

    def show_start_page(self):
        self.clear_window()
        self.refresh_page()
        label = tk.Label(self.root, text="Library Management", font=("Arial", 16))
        label.pack(pady=20)

        # Add Book Button
        add_book_button = tk.Button(self.root, text="Add book page", command=self.check_session_and_execute(self.show_add_book))
        add_book_button.pack(pady=10)

        # Remove Book Button
        remove_book_button = tk.Button(self.root, text="Remove Book", command=self.check_session_and_execute(self.show_remove_book))
        remove_book_button.pack(pady=10)

        # Search Book Button
        search_book_button = tk.Button(self.root, text="Search Book", command=self.check_session_and_execute(self.search_book))
        search_book_button.pack(pady=10)

        # View Books Button
        view_books_button = tk.Button(self.root, text="View Books", command=self.check_session_and_execute(self.view_books))
        view_books_button.pack(pady=10)

        # Lend Book Button
        lend_book_button = tk.Button(self.root, text="Lend Book", command=self.check_session_and_execute(self.show_lend_book))
        lend_book_button.pack(pady=10)

        # Return Book Button
        return_book_button = tk.Button(self.root, text="Return Book", command=self.check_session_and_execute(self.show_return_book))
        return_book_button.pack(pady=10)

        # Popular Books Button
        popular_books_button = tk.Button(self.root, text="Popular Books", command=self.check_session_and_execute(self.popular_books))
        popular_books_button.pack(pady=10)


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

                self.logging.info("logged in successfully")
            else:
                self.session = None
                messagebox.showerror("Login", "Invalid password!")
                self.logging.info("logged in fail")
        else:
            messagebox.showerror("Login", "Invalid username!")
            self.logging.info("logged in fail")
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

                new_user = {"username": librarian.get_username(), "password": librarian.get_password(), "notification": librarian.get_notification()}
                users_csv = users_csv._append(new_user, ignore_index=True)
                users_csv.to_csv("users.csv", index=False)

                self.session = {'librarian': librarian}

                messagebox.showinfo("Register", f"User '{username}' has been registered successfully!")
                self.show_start_page()

                self.logging.info("registered successfully")
            else:
                self.session = None
                messagebox.showerror("Register", "Passwords do not match!")
                self.logging.error("registered fail")
        else:
            messagebox.showerror("Register", "Username already registered!")
            self.logging.error("registered fail")
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
                                  command=lambda: (self.add_book( title_entry.get(), year_entry.get(), author_entry.get(),
                                                  genre_entry.get(), copy_entry.get())))
        submit_button.pack(pady=10)

        return_button = tk.Button(self.root, text="back", command=self.show_start_page)
        return_button.pack(pady=10)

    # Placeholder functions for the book actions
    def add_book(self,title, year, author, genre, copies):
        if not title.strip() or not author.strip() or not genre.strip() or not year.strip() or not copies.strip():
            messagebox.showerror("Input Error", "Title, Author, Genre, Year and copies cannot be empty.")
            self.logging.error("book added fail")
            return

        try:
            year = int(year)
            copies = int(copies)
        except ValueError:
            messagebox.showerror("Input Error", "Year and Copies must be valid a number.")
            self.logging.error("book added fail")
            return

        if year > 2025:
            messagebox.showerror("Input Error", "Year must be in the past.")
            self.logging.error("book added fail")
            return

        if copies <= 0:
            messagebox.showerror("Input Error", "Copies must be a positive number.")
            self.logging.error("book added fail")
            return
        book = BookFactory.create_book(title, author, False ,copies, year, genre,0,copies,"")
        self.session['librarian'].add_book(book)
        self.logging.info("book added successfully")
        messagebox.showinfo("Book Added", "Book added successfully!")
        self.show_start_page()


    def show_remove_book(self):
        self.clear_window()
        # Load the books from the file
        books_df = pd.read_csv('books.csv')
        books_list = books_df

        # Create a Listbox to display books
        book_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, height=20, width=75)
        for _, row in books_list.iterrows():
            book_display = f"{row['title']} by {row['author']} ({row['year']}, {row['genre']})"
            book_listbox.insert(tk.END, book_display)
        book_listbox.pack(padx=30, pady=30)

        borrow_button = tk.Button(self.root, text="Remove",
                                  command=lambda: self.remove_selected_book(book_listbox, books_list))
        borrow_button.pack(pady=10)
        # Function to handle book lending

        back_button = tk.Button(self.root, text="Back", command=self.show_start_page)
        back_button.pack(pady=10)

    def remove_selected_book(self, book_listbox, books_list):
        selected_index = book_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No book selected!")
            return

        selected_book = books_list.iloc[selected_index[0]]
        self.remove_book(selected_book)

    def remove_book(self, book):
        print(f"Removed: {book['title']} by {book['author']} ({book['year']}, {book['genre']})")
        remove_book = BookFactory.create_book(book['title'], book['author'], False, 0,
                                              book['year'], book['genre'], 0, 0,"")
        did_work = self.session['librarian'].remove_book(remove_book)
        if did_work:
            messagebox.showinfo("Remove Book", "The books was removed!")
            self.show_remove_book()
        else:
            messagebox.showerror("Remove Book", "All the copies of the book are loaned wait for 1 to return")


    def search_book(self):
        messagebox.showinfo("Search Book", "Search Book functionality")

    def view_books(self):
        self.clear_window()

        books_df = pd.read_csv('books.csv')
        books_list = books_df
        self.search_strategy = self.search_by_title
        book_listbox = tk.Listbox(self.root, selectmode=tk.DISABLED, height=20, width=75)
        for _, row in books_list.iterrows():
            book_display = f"{row['title']} by {row['author']} ({row['year']}, {row['genre']})"
            book_listbox.insert(tk.END, book_display)
        book_listbox.pack(padx=30, pady=30)


        # Create buttons to change search strategy
        title_button = tk.Button(self.root, text="Search by Title", command=self.search_by_title)
        title_button.pack(pady=5)

        author_button = tk.Button(self.root, text="Search by Author", command=self.search_by_author)
        author_button.pack(pady=5)

        genre_button = tk.Button(self.root, text="Search by Genre", command=self.search_by_genre)
        genre_button.pack(pady=5)

        search_entry = tk.Entry(self.root, width=40)
        search_entry.pack(pady=20)
        search_entry.bind("<KeyRelease>", lambda event: self.on_keyrelease(books_df, search_entry, book_listbox, False))

        return_button = tk.Button(self.root, text="back", command=self.show_start_page)
        return_button.pack(pady=10)

        self.logging.info("Displayed all books successfully")


    def show_lend_book(self):
        self.clear_window()

        # Load the books from the file
        books_df = pd.read_csv('books.csv')


        # Create a Listbox to display books
        book_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, height=20, width=75)
        for _, row in books_df.iterrows():
            book_display = f"{row['title']} by {row['author']} ({row['year']}, {row['genre']})"
            book_listbox.insert(tk.END, book_display)
        book_listbox.pack(padx=30, pady=30)

        phone_label = tk.Label(self.root, text="phone number:")
        phone_label.pack(pady=5)
        phone_entry = tk.Entry(self.root)
        phone_entry.pack(pady=5)

        borrow_button = tk.Button(self.root, text="Borrow", command=lambda: self.borrow_selected_book(book_listbox, books_df,phone_entry.get()))
        borrow_button.pack(pady=10)
        # Function to handle book lending

        back_button = tk.Button(self.root, text="Back", command=self.show_start_page)
        back_button.pack(pady=10)

        available_list = books_df[books_df['available_copies'] >= 1]
        available_button = tk.Button(self.root, text="Show_available", command=lambda: self.update_results_listbox(available_list,book_listbox))
        available_button.pack(pady=10)


        # Create buttons to change search strategy
        self.search_strategy = self.search_by_title
        title_button = tk.Button(self.root, text="Search by Title", command=self.search_by_title)
        title_button.pack(pady=5)

        author_button = tk.Button(self.root, text="Search by Author", command=self.search_by_author)
        author_button.pack(pady=5)

        genre_button = tk.Button(self.root, text="Search by Genre", command=self.search_by_genre)
        genre_button.pack(pady=5)

        search_entry = tk.Entry(self.root, width=40)
        search_entry.pack(pady=20)
        search_entry.bind("<KeyRelease>", lambda event: self.on_keyrelease(books_df, search_entry, book_listbox, True))

        # Static methods to perform the search

    def search_books_by_title(self,books_df, query):
        return books_df[books_df['title'].str.contains(query, case=False, na=False)]


    def search_books_by_author(self,books_df, query):
        return books_df[books_df['author'].str.contains(query, case=False, na=False)]


    def search_books_by_genre(self,books_df, query):
        return books_df[books_df['genre'].str.contains(query, case=False, na=False)]


    # Instance methods to change the search strategy
    def search_by_title(self):
        """Set search strategy to search by title."""
        self.logging.info("Search book by name completed successfully")
        self.search_strategy = self.search_books_by_title

    def search_by_author(self):
        """Set search strategy to search by author."""
        self.logging.info("Search book by author name completed successfully")
        self.search_strategy = self.search_books_by_author

    def search_by_genre(self):
        """Set search strategy to search by genre."""
        self.logging.info("Displayed book by category successfully")
        self.search_strategy = self.search_books_by_genre

    def on_keyrelease(self, books_df, search_entry, results_listbox, to_borrow):
        """Triggered every time the user types in the search entry."""
        query = search_entry.get()
        if to_borrow:
            all_books = books_df[books_df['available_copies'] > 1]
        else:
            all_books = books_df
        if query:
            # Perform search based on the selected strategy and update the Listbox
            if self.search_strategy:
                results = self.search_strategy(all_books, query)
                self.update_results_listbox(results, results_listbox)
        else:
            self.update_results_listbox(all_books, results_listbox)

    @staticmethod
    def update_results_listbox(results, listbox):
        listbox.delete(0, tk.END)  # Clear existing results
        for _, row in results.iterrows():
            book_info = f"{row['title']} by {row['author']} ({row['year']}, {row['genre']})"
            listbox.insert(tk.END, book_info)



    def borrow_selected_book(self, book_listbox, books_list,phone_number):
        selected_index = book_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No book selected!")
            self.logging.error("Book borrowed fail")
            return
        if not phone_number:
            messagebox.showerror("Error", "Must enter phone number!")
            self.logging.error("Book borrowed fail")
            return
        if not phone_number.isdigit():
            messagebox.showerror("Error", "Phone number must contain only digits!")
            self.logging.error("Book borrowed fail")
            return
        selected_book = books_list.iloc[selected_index[0]]
        self.lend_book(selected_book, str(phone_number))

    def lend_book(self, book, phone_number):
        print(f"Borrowed: {book['title']} by {book['author']} ({book['year']}, {book['genre']})")
        borrow_book = BookFactory.create_book(book['title'], book['author'], book['copies'],book['is_loaned'],book['year'], book['genre'],book['request'],book['available_copies'],book['queue'])
        did_work = self.session['librarian'].borrow_book(borrow_book, phone_number)
        if did_work == 1:
            messagebox.showinfo("Lend Book", "The book has been borrowed successfully!")
            self.logging.info("Book borrowed successfully")
            self.show_lend_book()
        elif did_work == 2:
            messagebox.showinfo("Lend Book", "No available copies you were added to the queue!")
            self.logging.info("Book borrowed fail")
            self.show_lend_book()
        else:
            messagebox.showerror("Error", "You are already in queue")
            self.logging.error("Book borrowed fail")

    def show_return_book(self):
        self.clear_window()
        # Load the books from the file
        loaned_books_df = pd.read_csv('Loaned_books.csv')
        books_list = loaned_books_df

        # Create a Listbox to display books
        book_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, height=20, width=75)
        for _, row in books_list.iterrows():
            book_display = f"{row['title']} by {row['author']} ({row['year']}, {row['genre']}, {row['phone_number']})"
            book_listbox.insert(tk.END, book_display)
        book_listbox.pack(padx=30, pady=30)

        borrow_button = tk.Button(self.root, text="Return",
                                  command=lambda: self.return_selected_book(book_listbox, books_list))
        borrow_button.pack(pady=10)
        # Function to handle book lending

        back_button = tk.Button(self.root, text="Back", command=self.show_start_page)
        back_button.pack(pady=10)

    def return_selected_book(self, book_listbox, books_list):
        selected_index = book_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No book selected!")
            return

        selected_book = books_list.iloc[selected_index[0]]
        self.return_book(selected_book)

    def return_book(self, book):
        print(f"Returned: {book['title']} by {book['author']} ({book['year']}, {book['genre']}, {book['phone_number']})")
        return_book = BookFactory.create_book(book['title'], book['author'], False, 0,
                                              book['year'], book['genre'], 0, 0,"")
        did_work = self.session['librarian'].return_book(return_book, book['phone_number'])
        if did_work:
            messagebox.showinfo("Return Book", "The book has been returned successfully!")
            self.logging.info("Book returned successfully")
            self.show_return_book()
        else:
            messagebox.showerror("Error", "The book was not returned!")
            self.logging.error("Book returned fail")

    def popular_books(self):
        self.clear_window()
        df = pd.read_csv('books.csv')
        top_books = df.sort_values(by='request', ascending=False).head(10)
        book_listbox = tk.Listbox(self.root, selectmode=tk.DISABLED, height=20, width=75)
        for _, row in top_books.iterrows():
            book_display = f"{row['title']} by {row['author']} ({row['year']}, {row['genre']})"
            book_listbox.insert(tk.END, book_display)
        book_listbox.pack(padx=30, pady=30)
        self.logging.info("displayed successfully")

    def check_session_and_execute(self, func):
        def wrapper(*args, **kwargs):
            if self.session is None:
                messagebox.showerror("Error", "Session not active. Please log in first.")
                self.logging.error("Session not active. Please log in first.")
            else:
                return func(*args, **kwargs)

        return wrapper


