
from werkzeug.security import generate_password_hash

from Menagment.books.bookFactory import BookFactory
from Menagment.books.book import *

class Librarians:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)


    def get_password(self):
        return self.password_hash
    def get_username(self):
        return self.username

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
                books_df.to_csv('books.csv', index=False)
                return 1

            queue_value = books_df.at[index, 'queue']

            if pd.isna(queue_value) or queue_value == "":
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

            loaned_books = loaned_books.drop(loaned_row.index)

            # Save the updated books and loaned_books DataFrames back to the CSVs
            books_df.to_csv('books.csv', index=False)
            loaned_books.to_csv('loaned_books.csv', index=False)
            return True
        return False


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
                elif books_df.at[index, 'available_copies'] == 0:
                    books_df.at[index, 'is_loaned'] = 'Yes'
                books_df.to_csv('books.csv', index=False)
                return True
            else:
                print('all the books are loaned wait until at least 1 is returned')
                return False


