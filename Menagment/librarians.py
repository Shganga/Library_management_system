import ast
import tkinter
from xmlrpc.client import FastParser

from werkzeug.security import generate_password_hash

from Menagment.books.bookFactory import BookFactory
from Menagment.books.book import *
from notification import Notification


class Librarians(Notification):
    def __init__(self, username, password):
        self.__username = username
        self.__password_hash = generate_password_hash(password)



    def get_password(self):
        return self.__password_hash
    def get_username(self):
        return self.__username


    def notify(self, message):
        user_csv = pd.read_csv('users.csv')

        for index, row in user_csv.iterrows():
            current_notifications = row['notification']

            # If the current notifications are NaN (empty), initialize as an empty list
            if pd.isna(current_notifications):
                current_notifications = []
            elif isinstance(current_notifications, str):
                # Convert string to list if it's a string representation of a list
                try:
                    current_notifications = ast.literal_eval(current_notifications)
                    if not isinstance(current_notifications, list):
                        current_notifications = []  # If it's not a list, reset it
                except:
                    current_notifications = []  # If conversion fails, reset to an empty list

            # Append the new message to the list
            current_notifications.append(message)

            # Ensure that the notification column holds a list, not a string
            user_csv.at[index, 'notification'] = current_notifications

        # Save the updated DataFrame back to the CSV
        user_csv.to_csv('users.csv', index=False)

    def borrow_book(self,book,phone_number):
        books_df = pd.read_csv('books.csv')
        book_row = books_df[(books_df['title'] == book.get_title()) & (books_df['author'] == book.get_author()) & (
                    books_df['year'] == book.get_year()) & (books_df['genre'] == book.get_genre())]
        if not book_row.empty:
            index = book_row.index[0]
            if book_row['available_copies'].values[0] > 0:
                loaned_books = pd.read_csv("loaned_books.csv")
                new_loan = {
                    'title': book.get_title(),
                    'author': book.get_author(),
                    'year': book.get_year(),
                    'genre': book.get_genre(),
                    'phone_number': phone_number
                }
                loaned_books = pd.concat([loaned_books, pd.DataFrame([new_loan])], ignore_index=True)
                loaned_books.to_csv('loaned_books.csv', index=False)


                books_df.at[index, 'available_copies'] -= 1
                books_df.at[index, 'request'] += 1

                if books_df.at[index,'available_copies'] == 0:
                    if books_df.at[index, 'is_loaned'] != 'Yes':
                        books_df.at[index, 'is_loaned'] = 'Yes'

                self.notify(f"The user: {self.get_username()} lent the book {book.get_title()} by {book.get_author()} to {phone_number}.")

                books_df.to_csv('books.csv', index=False)
                return 1

            queue_value = books_df.at[index, 'queue']

            if pd.isna(queue_value) or queue_value == "" or queue_value.strip(',') == '':
                books_df['queue'] = books_df['queue'].astype(str)
                books_df.at[index, 'queue'] = str(phone_number) + ','
                books_df.to_csv('books.csv', index=False)
                return 2  # Phone number added to queue

            else:
                # Split the queue (comma-separated list of phone numbers)
                queue_list = str(queue_value).split(',') if queue_value else []

                queue_list = [number for number in queue_list if number]  # Filter out any empty string

                # Add phone number to queue if not already present
                if str(phone_number) not in queue_list:
                    queue_list.append(str(phone_number))
                    # Append phone number as text
                    books_df.at[index, 'queue'] = ','.join(queue_list)  # Update the queue column

                    books_df.to_csv('books.csv', index=False)
                    return 2  # Phone number added to queue
        return 0


    def return_book(self,book,phone_number):
        loaned_books = pd.read_csv("loaned_books.csv")
        books_df = pd.read_csv('books.csv')
        loaned_row = loaned_books[(loaned_books['phone_number'] == phone_number) & (loaned_books['title'] == book.get_title()) &
                            (loaned_books['author'] == book.get_author()) & (loaned_books['year'] == book.get_year()) & (loaned_books['genre'] == book.get_genre())]
        if not loaned_row.empty:
            # Increase the available copies by 1
            book_row = books_df[(books_df['title'] == book.get_title()) & (books_df['author'] == book.get_author()) & (
                    books_df['year'] == book.get_year()) & (books_df['genre'] == book.get_genre())]
            if not book_row.empty:
                book_index = book_row.index[0]

                # Update the available copies and is_loaned field
                books_df.at[book_index, 'available_copies'] += 1
                if books_df.at[book_index, 'available_copies'] > 0:
                    books_df.at[book_index, 'is_loaned'] = 'No'
                loaned_books = loaned_books.drop(loaned_row.index[0])
                books_df.to_csv('books.csv', index=False)
                loaned_books.to_csv('loaned_books.csv', index=False)
                self.notify(
                    f"{phone_number} returned the book {book.get_title()} by {book.get_author()} to {self.get_username()}.")

                self.handle_queue(book)



            return True
        return False

    def handle_queue(self,book):
        books_df = pd.read_csv('books.csv')
        book_row = books_df[(books_df['title'] == book.get_title()) & (books_df['author'] == book.get_author()) & (
                books_df['year'] == book.get_year()) & (books_df['genre'] == book.get_genre())]
        book_index = book_row.index[0]
        queue_string = books_df.at[book_index, 'queue']
        if pd.notna(queue_string) and queue_string.strip() and queue_string.strip(',') != '':
            phone_numbers = queue_string.split(',')
            first_phone_number = phone_numbers[0]
            phone_numbers.pop(0)
            phone_numbers = [number for number in phone_numbers if number]
            updated_queue_string = ','.join(phone_numbers)
            books_df.at[book_index, 'queue'] = updated_queue_string + ','
            books_df.to_csv('books.csv', index=False)
            self.borrow_book(book, first_phone_number)



    def add_book(self,book):
        books_df = pd.read_csv('books.csv')
        book_row = books_df[(books_df['title'] == book.get_title()) & (books_df['author'] == book.get_author()) & (books_df['year'] == book.get_year()) & (books_df['genre'] == book.get_genre())]
        if book_row.empty:
            books_df = books_df._append(book.to_dict(), ignore_index=True)
        else:
            row_index = book_row.index[0]
            books_df.at[row_index, 'copies'] += book.get_copies()
            books_df.at[row_index, 'available_copies'] += book.get_copies()
        books_df.to_csv('books.csv', index=False)
        self.notify(
            f"User: {self.get_username()} added a new book {book.get_title()} by {book.get_author()} genre {book.get_genre()} year {book.get_year()} copies of book {book.get_copies()}.")

    def remove_book(self,book):
        books_df = pd.read_csv('books.csv')
        book_row = books_df[(books_df['title'] == book.get_title()) & (books_df['author'] == book.get_author()) & (
                    books_df['year'] == book.get_year()) & (books_df['genre'] == book.get_genre())]
        index = book_row.index[0]
        if not book_row.empty:
            if books_df.at[index, 'is_loaned'] == 'No':
                books_df.at[index, 'available_copies'] -= 1
                books_df.at[index, 'copies'] -= 1
                if books_df.at[index, 'copies'] == 0:
                    books_df = books_df.drop(index)
                    self.notify(
                        f"User: {self.get_username()} removed the book {book.get_title()} by {book.get_author()} genre {book.get_genre()} year {book.get_year()}")
                elif books_df.at[index, 'available_copies'] == 0:
                    books_df.at[index, 'is_loaned'] = 'Yes'
                    self.notify(
                        f"User: {self.get_username()} removed a copy of the book {book.get_title()} by {book.get_author()} genre {book.get_genre()} year {book.get_year()}")
                else:
                    self.notify(f"User: {self.get_username()} removed a copy of the book {book.get_title()} by {book.get_author()} genre {book.get_genre()} year {book.get_year()}")
                books_df.to_csv('books.csv', index=False)

                return True
            else:
                print('all the books are loaned wait until at least 1 is returned')
                return False

    def remove_notification(self, notification_index):
        # If notification_index is a tuple, just take the first element
        if isinstance(notification_index, tuple):
            notification_index = notification_index[0]

        # Load the users CSV and find the user
        users_df = pd.read_csv('users.csv')
        user_row = users_df[users_df["username"] == self.__username]

        if not user_row.empty:
            # Get the current notifications and ensure it's a list
            current_notifications = user_row["notification"].values[0]
            try:
                current_notifications = ast.literal_eval(current_notifications) if isinstance(current_notifications,
                                                                                              str) else current_notifications
            except:
                current_notifications = []

            # Remove the notification if index is valid
            if 0 <= notification_index < len(current_notifications):
                current_notifications.pop(notification_index)
                users_df.at[user_row.index[0], 'notification'] = current_notifications
                users_df.to_csv('users.csv', index=False)
                return True
        return False

