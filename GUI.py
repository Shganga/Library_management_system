import ast
import tkinter as tk
from functools import partial
from re import search
from tkinter import messagebox, ttk
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
        self.main_color = tk.StringVar(value='#ffffff')
        self.secondary_color = tk.StringVar(value='#0e6251')
        self.root.configure(background=self.main_color.get())
        self.user_bar = tk.Frame(self.root, height=40, bg=self.secondary_color.get())
        self.user_bar.pack(side="top", fill="x")

        self.title_frame = tk.Frame(self.user_bar, bg=self.secondary_color.get())
        self.title_frame.pack(side="top", fill="x")

        self.title_label = tk.Label(self.title_frame, text="Library System", font=("Arial", 16), bg=self.secondary_color.get(), fg=self.main_color.get())
        self.title_label.pack(side="top",anchor="center", fill="x")
        self.login_button = tk.Button(self.user_bar, text="login",background=self.main_color.get() , foreground=self.secondary_color.get(), command=self.show_login_page)
        self.register_button = tk.Button(self.user_bar, text="Register",background=self.main_color.get(), foreground=self.secondary_color.get(), command=self.show_register_page)
        self.logout_button = tk.Button(self.user_bar, text="Logout",background=self.main_color.get(), foreground=self.secondary_color.get(), command=self.logout)
        self.notify_button = tk.Button(self.user_bar, text="💬",background=self.main_color.get(), foreground=self.secondary_color.get(), command=self.show_notifications)
        self.home_button = tk.Button(self.user_bar, text="🏠", background=self.main_color.get(), foreground=self.secondary_color.get(), command=self.show_start_page)

        # Start the application
        self.refresh_page()
        self.show_start_page()


    def refresh_page(self):
        if self.session is None:
            self.login_button.pack(pady=10, side="right", padx=5 )
            self.register_button.pack(pady=10,side="right", padx=5)
            self.notify_button.pack_forget()
            self.logout_button.pack_forget()
            self.home_button.pack_forget()
        else:
            self.logout_button.pack(pady=10,side="right", padx=5)
            self.notify_button.pack(pady=10, side="right", padx=5)
            self.home_button.pack(pady=10, side="left", padx=10)
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
        self.title_label.config(text="Notifications")

        # Load the user's notifications from the CSV
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

        # Create a Treeview to display notifications
        tree = ttk.Treeview(self.root, columns=("Notification"), show="headings", height=10)
        tree.pack(pady=20)

        # Define columns
        tree.heading("Notification", text="Notification")
        tree.column("Notification", width=500)

        # Add a scrollbar for the Treeview
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=tree.yview)
        tree.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Add each notification as a row in the Treeview
        for notification in notifications:
            tree.insert("", "end", values=(notification,))

        # Optional: you can add a message if there are no notifications
        if not notifications:
            tree.insert("", "end", values=("No notifications available.",))

        # Add a delete button for removing notifications
        delete_msg_button = tk.Button(self.root, text="Delete", background=self.secondary_color.get(),
                                      foreground=self.main_color.get(), command=lambda: self.delete_notification(tree))
        delete_msg_button.pack(anchor="center", padx=5, pady=5)

    def delete_notification(self, tree):
        # Get the selected item in the Treeview
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No notification selected!")
            return

        # Get the index of the selected item
        selected_index = tree.index(selected_item)

        # Call the remove_notification method with the selected index
        did_work = self.session['librarian'].remove_notification(selected_index)
        if did_work:
            messagebox.showinfo("Success", "Notification was deleted")
            self.show_notifications()  # Refresh the notifications
        else:
            messagebox.showerror("Error", "Something went wrong")

    def show_start_page(self):
        self.clear_window()
        self.refresh_page()
        self.title_label.config(text="Library System")

        # Frame to center everything
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill="both")

        # Frame for buttons, center this inside main_frame
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(side="top", expand=True, pady=10)

        # Create buttons and place them in a centered layout

        # Row 1 Frame
        row1_frame = tk.Frame(buttons_frame)
        row1_frame.pack(side="top", pady=15)

        # Add Book Button
        add_book_button = tk.Button(row1_frame, width=30, height=3,font=("Arial", 12), text="Add Book Page",
                                    background=self.secondary_color.get(), foreground=self.main_color.get(),
                                    command=self.check_session_and_execute(self.show_add_book))
        add_book_button.pack(side="left", padx=10)

        # Remove Book Button
        remove_book_button = tk.Button(row1_frame, width=30, height=3,font=("Arial", 12), text="Remove Book",
                                       background=self.secondary_color.get(), foreground=self.main_color.get(),
                                       command=self.check_session_and_execute(self.show_remove_book))
        remove_book_button.pack(side="left", padx=10)

        # View Books Button
        view_books_button = tk.Button(row1_frame, width=30, height=3,font=("Arial", 12), text="View Books",
                                      background=self.secondary_color.get(), foreground=self.main_color.get(),
                                      command=self.check_session_and_execute(self.view_books))
        view_books_button.pack(side="left", padx=10)

        # Row 2 Frame
        row2_frame = tk.Frame(buttons_frame)
        row2_frame.pack(side="top", pady=15)

        # Lend Book Button
        lend_book_button = tk.Button(row2_frame, width=30, height=3,font=("Arial", 12), text="Lend Book",
                                     background=self.secondary_color.get(), foreground=self.main_color.get(),
                                     command=self.check_session_and_execute(self.show_lend_book))
        lend_book_button.pack(side="left", padx=10)

        # Return Book Button
        return_book_button = tk.Button(row2_frame, width=30, height=3,font=("Arial", 12), text="Return Book",
                                       background=self.secondary_color.get(), foreground=self.main_color.get(),
                                       command=self.check_session_and_execute(self.show_return_book))
        return_book_button.pack(side="left", padx=10)

        # Popular Books Button
        popular_books_button = tk.Button(row2_frame, width=30, height=3,font=("Arial", 12), text="Popular Books",
                                         background=self.secondary_color.get(), foreground=self.main_color.get(),
                                         command=self.check_session_and_execute(self.popular_books))
        popular_books_button.pack(side="left", padx=10)





    def show_login_page(self):
        self.clear_window()
        self.title_label.config(text="Login")
        label = tk.Label(self.root, text="Login",bg=self.main_color.get(), fg=self.secondary_color.get(),  font=("Arial", 16))
        label.pack(pady=20)

        username_label = tk.Label(self.root,bg=self.main_color.get(), fg=self.secondary_color.get(),  text="Username:")
        username_label.pack(pady=5)
        username_entry = tk.Entry(self.root)
        username_entry.pack(pady=5)

        password_label = tk.Label(self.root,bg=self.main_color.get(), fg=self.secondary_color.get(),  text="Password:")
        password_label.pack(pady=5)
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack(pady=5)

        login_button = tk.Button(self.root, text="Login",background=self.secondary_color.get() , foreground=self.main_color.get(),
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
        self.title_label.config(text="Register")
        label = tk.Label(self.root, text="Register",bg=self.main_color.get(), fg=self.secondary_color.get(),  font=("Arial", 16))
        label.pack(pady=20)

        username_label = tk.Label(self.root,bg=self.main_color.get(), fg=self.secondary_color.get(),  text="Username:")
        username_label.pack(pady=5)
        username_entry = tk.Entry(self.root)
        username_entry.pack(pady=5)

        password_label = tk.Label(self.root,bg=self.main_color.get(), fg=self.secondary_color.get(),  text="Password:")
        password_label.pack(pady=5)
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack(pady=5)

        confirm_password_label = tk.Label(self.root,bg=self.main_color.get(), fg=self.secondary_color.get(),  text="Confirm Password:")
        confirm_password_label.pack(pady=5)
        confirm_password_entry = tk.Entry(self.root, show="*")
        confirm_password_entry.pack(pady=5)

        register_button = tk.Button(self.root, text="Register",background=self.secondary_color.get() , foreground=self.main_color.get(), command=lambda: self.register(username_entry.get(), password_entry.get(), confirm_password_entry.get()))
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
        self.title_label.config(text="Add book")
        # Create the login page widgets
        label = tk.Label(self.root, text="add book",bg=self.main_color.get(), fg=self.secondary_color.get(),  font=("Arial", 16))
        label.pack(pady=20)

        title_label = tk.Label(self.root,bg=self.main_color.get(), fg=self.secondary_color.get(),  text="title:")
        title_label.pack(pady=5)
        title_entry = tk.Entry(self.root)
        title_entry.pack(pady=5)

        year_label = tk.Label(self.root,bg=self.main_color.get(), fg=self.secondary_color.get(),  text="year:")
        year_label.pack(pady=5)
        year_entry = tk.Entry(self.root)
        year_entry.pack(pady=5)

        author_label = tk.Label(self.root,bg=self.main_color.get(), fg=self.secondary_color.get(),  text="author:")
        author_label.pack(pady=5)
        author_entry = tk.Entry(self.root)
        author_entry.pack(pady=5)

        genre_label = tk.Label(self.root,bg=self.main_color.get(), fg=self.secondary_color.get(),  text="genre:")
        genre_label.pack(pady=5)
        genre_entry = tk.Entry(self.root)
        genre_entry.pack(pady=5)

        copy_label = tk.Label(self.root,bg=self.main_color.get(), fg=self.secondary_color.get(),  text="copy:")
        copy_label.pack(pady=5)
        copy_entry = tk.Entry(self.root)
        copy_entry.pack(pady=5)

        submit_button = tk.Button(self.root, text="add",background=self.secondary_color.get() , foreground=self.main_color.get(),
                                  command=lambda: (self.add_book( title_entry.get(), year_entry.get(), author_entry.get(),
                                                  genre_entry.get(), copy_entry.get())))
        submit_button.pack(pady=10)

        # return_button = tk.Button(self.root, text="🏠",background=self.secondary_color.get() , foreground=self.main_color.get(), command=self.show_start_page)
        # return_button.pack(pady=10)

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
        self.title_label.config(text="Remove Book")

        # Load the books from the file
        books_df = pd.read_csv('books.csv')

        # Create a Treeview to display books
        tree = ttk.Treeview(self.root, columns=("Title", "Author", "Year", "Genre"), show="headings", height=20)
        tree.pack(padx=30, pady=30, fill=tk.BOTH, expand=True)

        # Define column headings and widths
        tree.heading("Title", text="Title")
        tree.column("Title", anchor=tk.W, width=200)

        tree.heading("Author", text="Author")
        tree.column("Author", anchor=tk.W, width=150)

        tree.heading("Year", text="Year")
        tree.column("Year", anchor=tk.W, width=80)

        tree.heading("Genre", text="Genre")
        tree.column("Genre", anchor=tk.W, width=120)

        for _, row in books_df.iterrows():
            tree.insert("", tk.END, values=(row["title"], row["author"], row["year"], row["genre"]))

        remove_button = tk.Button(self.root, text="Remove", background=self.secondary_color.get(),
                                  foreground=self.main_color.get(),
                                  command=lambda: self.remove_selected_book(tree, books_df))
        remove_button.pack(pady=10)

    def remove_selected_book(self, book_treeview, books_list):
        selected_item = book_treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "No book selected!")
            return
        selected_index = int(book_treeview.index(selected_item[0]))
        selected_book = books_list.iloc[selected_index]

        self.remove_book(selected_book)


    def remove_book(self, book):
        print(f"Removed: {book['title']} by {book['author']} ({book['year']}, {book['genre']})")
        remove_book = BookFactory.create_book(book['title'], book['author'], False, 0,
                                              book['year'], book['genre'], 0, 0,"")
        did_work = self.session['librarian'].remove_book(remove_book)
        if did_work:
            messagebox.showinfo("Remove Book", "The books was removed!")
            self.logging.info("book removed successfully")
            self.show_remove_book()
        else:
            messagebox.showerror("Remove Book", "All the copies of the book are loaned wait for 1 to return")
            self.logging.info("book removed fail")


    def search_book(self):
        messagebox.showinfo("Search Book", "Search Book functionality")

    def view_books(self):
        self.clear_window()
        self.title_label.config(text="View Books")
        books_df = pd.read_csv('books.csv')
        top_frame = tk.Frame(self.root, bg=self.main_color.get())
        top_frame.pack()
        # Button to show available books
        available_list = books_df[books_df['available_copies'] >= 1]
        available_button = tk.Button(top_frame, text="Show Available", background=self.secondary_color.get(),
                                     foreground=self.main_color.get(),
                                     command=lambda: self.show_available_books(available_list, tree))
        available_button.pack(pady=10, side="left")

        # Button to show loaned books
        loaned_list = books_df[books_df['is_loaned'] == 'Yes']
        loaned_button = tk.Button(top_frame, text="Show Loaned", background=self.secondary_color.get(),
                                  foreground=self.main_color.get(),
                                  command=lambda: self.show_loaned_books(loaned_list, tree))
        loaned_button.pack(pady=10, side="left")

        # Button to show all books
        all_button = tk.Button(top_frame, text="Show All", background=self.secondary_color.get(),
                               foreground=self.main_color.get(), command=lambda: self.show_all_books(books_df, tree))
        all_button.pack(pady=10, side="left")
        # Create a Treeview widget for displaying books
        tree = ttk.Treeview(self.root, columns=("Title", "Author", "Year", "Genre"), show="headings", height=20)
        tree.pack(padx=30, pady=30, fill=tk.BOTH, expand=True)

        # Define column headings and widths
        tree.heading("Title", text="Title")
        tree.column("Title", anchor=tk.W, width=200)

        tree.heading("Author", text="Author")
        tree.column("Author", anchor=tk.W, width=150)

        tree.heading("Year", text="Year")
        tree.column("Year", anchor=tk.W, width=80)

        tree.heading("Genre", text="Genre")
        tree.column("Genre", anchor=tk.W, width=120)

        # Populate the Treeview with book data
        for _, row in books_df.iterrows():
            tree.insert("", tk.END, values=(row["title"], row["author"], row["year"], row["genre"]))

        # Create a button frame for search options
        button_frame = tk.Frame(self.root, bg=self.main_color.get())
        button_frame.pack()

        # Search buttons and entry
        search_entry = tk.Entry(button_frame, width=40)
        search_entry.pack(pady=20, side="left")

        title_button = tk.Button(button_frame, text="Search by Title", background=self.secondary_color.get(),
                                 foreground=self.main_color.get(),
                                 command=lambda: self.search_by_title(books_df, search_entry, tree))
        title_button.pack(side="left", pady=5, padx=5)

        author_button = tk.Button(button_frame, text="Search by Author", background=self.secondary_color.get(),
                                  foreground=self.main_color.get(),
                                  command=lambda: self.search_by_author(books_df, search_entry, tree))
        author_button.pack(side="left", pady=5, padx=5)

        genre_button = tk.Button(button_frame, text="Search by Genre", background=self.secondary_color.get(),
                                 foreground=self.main_color.get(),
                                 command=lambda: self.search_by_genre(books_df, search_entry, tree))
        genre_button.pack(side="left", pady=5, padx=5)



        self.logging.info("Displayed all books.")

    def show_available_books(self, available_list, tree):
        # Update Treeview with available books
        self.update_results_treeview(available_list, tree)
        self.logging.info("Displayed available books.")

    def show_loaned_books(self, loaned_list, tree):
        # Update Treeview with loaned books
        self.update_results_treeview(loaned_list, tree)
        self.logging.info("Displayed loaned books.")

    def show_all_books(self, books_df, tree):
        # Update Treeview with all books
        self.update_results_treeview(books_df, tree)
        self.logging.info("Displayed all books.")

    def show_lend_book(self):
        self.clear_window()
        self.title_label.config(text="Lend Book")

        # Load the books from the file
        books_df = pd.read_csv('books.csv')

        # Create a frame for search buttons and entry
        button_frame = tk.Frame(self.root, bg=self.main_color.get())
        button_frame.pack(side="top")

        search_entry = tk.Entry(button_frame, width=40)
        search_entry.pack(pady=20, side="left")

        title_button = tk.Button(button_frame, text="Search by Title", background=self.secondary_color.get(),
                                 foreground=self.main_color.get(),
                                 command=lambda: self.search_by_title(books_df, search_entry, tree))
        title_button.pack(side="left", pady=5, padx=5)

        author_button = tk.Button(button_frame, text="Search by Author", background=self.secondary_color.get(),
                                  foreground=self.main_color.get(),
                                  command=lambda: self.search_by_author(books_df, search_entry, tree))
        author_button.pack(side="left", pady=5, padx=5)

        genre_button = tk.Button(button_frame, text="Search by Genre", background=self.secondary_color.get(),
                                 foreground=self.main_color.get(),
                                 command=lambda: self.search_by_genre(books_df, search_entry, tree))
        genre_button.pack(side="left", pady=5, padx=5)
        # Create a Treeview to display books
        tree = ttk.Treeview(self.root, columns=("Title", "Author", "Year", "Genre", "Available Copies"),
                            show="headings", height=20)
        tree.pack(padx=30, pady=30, fill=tk.BOTH, expand=True)

        # Define column headings and widths
        tree.heading("Title", text="Title")
        tree.column("Title", anchor=tk.W, width=200)

        tree.heading("Author", text="Author")
        tree.column("Author", anchor=tk.W, width=150)

        tree.heading("Year", text="Year")
        tree.column("Year", anchor=tk.W, width=80)

        tree.heading("Genre", text="Genre")
        tree.column("Genre", anchor=tk.W, width=120)

        tree.heading("Available Copies", text="Available Copies")
        tree.column("Available Copies", anchor=tk.W, width=120)

        # Populate the Treeview with books
        for _, row in books_df.iterrows():
            tree.insert("", tk.END,
                        values=(row["title"], row["author"], row["year"], row["genre"], row["available_copies"]))



        button_frame2 = tk.Frame(self.root, bg=self.main_color.get())
        button_frame2.pack()
        # Phone number entry and label
        phone_label = tk.Label(button_frame2, bg=self.main_color.get(), fg=self.secondary_color.get(), text="Phone number:")
        phone_label.pack(pady=5,side="left", padx=5)
        phone_entry = tk.Entry(button_frame2)
        phone_entry.pack(pady=5, side="left")

        # Borrow button
        borrow_button = tk.Button(button_frame2, text="Borrow", background=self.secondary_color.get(),
                                  foreground=self.main_color.get(),
                                  command=lambda: self.borrow_selected_book(tree, books_df, phone_entry.get()))
        borrow_button.pack(pady=10, side="left")


    def search_books_by_title(self,books_df, query):
        return books_df[books_df['title'].str.contains(query, case=False, na=False)]


    def search_books_by_author(self,books_df, query):
        return books_df[books_df['author'].str.contains(query, case=False, na=False)]


    def search_books_by_genre(self,books_df, query):
        return books_df[books_df['genre'].str.contains(query, case=False, na=False)]


    # Instance methods to change the search strategy
    def search_by_title(self, books_df, search_entry, results_listbox):
        """Set search strategy to search by title."""
        self.search_strategy = self.search_books_by_title
        self.search_button_pressed(books_df, search_entry, results_listbox, False)
        self.logging.info(f"Search book \"{search_entry.get()}\" by name completed successfully")

    def search_by_author(self, books_df, search_entry, results_listbox):
        """Set search strategy to search by author."""
        self.search_strategy = self.search_books_by_author
        self.search_button_pressed(books_df, search_entry, results_listbox, False)
        self.logging.info(f"Search book by author name \"{search_entry.get()}\" completed successfully")


    def search_by_genre(self, books_df, search_entry, results_listbox):
        """Set search strategy to search by genre."""
        self.search_strategy = self.search_books_by_genre
        self.search_button_pressed(books_df, search_entry, results_listbox, False)
        self.logging.info(f"Displayed book by category \"{search_entry.get()}\" successfully")



    def search_button_pressed(self, books_df, search_entry, results_treeview, to_borrow):
        query = search_entry.get()
        # Filter books based on availability if `to_borrow` is True
        if to_borrow:
            all_books = books_df[books_df['available_copies'] > 1]
        else:
            all_books = books_df

        # Clear the Treeview
        results_treeview.delete(*results_treeview.get_children())

        # Perform search and update the Treeview
        if query:
            # Use the selected search strategy to filter results
            if self.search_strategy:
                results = self.search_strategy(all_books, query)
                self.update_results_treeview(results, results_treeview)
        else:
            # If no query, display all books
            self.update_results_treeview(all_books, results_treeview)

    def update_results_treeview(self, results_df, treeview):
        # Clear the Treeview
        treeview.delete(*treeview.get_children())

        # Populate the Treeview with results
        for _, row in results_df.iterrows():
            treeview.insert("", tk.END, values=(row["title"], row["author"], row["year"], row["genre"]))

    @staticmethod
    def update_results_listbox(results, listbox):
        listbox.delete(0, tk.END)  # Clear existing results
        for _, row in results.iterrows():
            book_info = f"{row['title']} by {row['author']} ({row['year']}, {row['genre']})"
            listbox.insert(tk.END, book_info)

    def borrow_selected_book(self, book_treeview, books_list, phone_number):
        # Get selected item from the Treeview
        selected_item = book_treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "No book selected!")
            self.logging.error("Book borrow failed: No book selected.")
            return

        # Validate phone number
        if not phone_number:
            messagebox.showerror("Error", "Must enter phone number!")
            self.logging.error("Book borrow failed: Phone number missing.")
            return
        if not phone_number.isdigit():
            messagebox.showerror("Error", "Phone number must contain only digits!")
            self.logging.error("Book borrow failed: Invalid phone number.")
            return

        # Get the index of the selected book
        selected_index = int(book_treeview.index(selected_item[0]))
        selected_book = books_list.iloc[selected_index]

        # Lend the selected book
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
        self.title_label.config(text="Return Book")

        # Load the books from the file
        loaned_books_df = pd.read_csv('Loaned_books.csv')

        # Create a Treeview to display loaned books
        tree = ttk.Treeview(self.root, columns=("Title", "Author", "Year", "Genre", "Phone Number"), show="headings",
                            height=20)
        tree.pack(padx=30, pady=30, fill=tk.BOTH, expand=True)

        # Define column headings and widths
        tree.heading("Title", text="Title")
        tree.column("Title", anchor=tk.W, width=200)

        tree.heading("Author", text="Author")
        tree.column("Author", anchor=tk.W, width=150)

        tree.heading("Year", text="Year")
        tree.column("Year", anchor=tk.W, width=80)

        tree.heading("Genre", text="Genre")
        tree.column("Genre", anchor=tk.W, width=120)

        tree.heading("Phone Number", text="Phone Number")
        tree.column("Phone Number", anchor=tk.W, width=150)

        # Populate the Treeview with loaned books
        for _, row in loaned_books_df.iterrows():
            tree.insert("", tk.END,
                        values=(row["title"], row["author"], row["year"], row["genre"], row["phone_number"]))

        # Create the return button
        return_button = tk.Button(self.root, text="Return", background=self.secondary_color.get(),
                                  foreground=self.main_color.get(),
                                  command=lambda: self.return_selected_book(tree, loaned_books_df))
        return_button.pack(pady=10)

    def return_selected_book(self, book_treeview, books_list):
        # Get the selected item from the Treeview
        selected_item = book_treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "No book selected!")
            return

        selected_index = int(book_treeview.index(selected_item[0]))
        selected_book = books_list.iloc[selected_index]

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
        self.title_label.config(text="Popular Books")

        # Load the books from the file
        df = pd.read_csv('books.csv')

        # Sort books by 'request' and get the top 10 most popular books
        top_books = df.sort_values(by='request', ascending=False).head(10)

        # Create a Treeview to display popular books
        tree = ttk.Treeview(self.root, columns=("Title", "Author", "Year", "Genre", "Requests"), show="headings",
                            height=20)
        tree.pack(padx=30, pady=30, fill=tk.BOTH, expand=True)

        # Define column headings and widths
        tree.heading("Title", text="Title")
        tree.column("Title", anchor=tk.W, width=200)

        tree.heading("Author", text="Author")
        tree.column("Author", anchor=tk.W, width=150)

        tree.heading("Year", text="Year")
        tree.column("Year", anchor=tk.W, width=80)

        tree.heading("Genre", text="Genre")
        tree.column("Genre", anchor=tk.W, width=120)

        tree.heading("Requests", text="Requests")
        tree.column("Requests", anchor=tk.W, width=80)

        # Populate the Treeview with the top 10 popular books
        for _, row in top_books.iterrows():
            tree.insert("", tk.END, values=(row["title"], row["author"], row["year"], row["genre"], row["request"]))

        self.logging.info("Displayed popular books successfully")

    def check_session_and_execute(self, func):
        def wrapper(*args, **kwargs):
            if self.session is None:
                messagebox.showerror("Error", "Session not active. Please log in first.")
                self.logging.error("Session not active. Please log in first.")
            else:
                return func(*args, **kwargs)

        return wrapper


