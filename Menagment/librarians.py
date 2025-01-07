
from werkzeug.security import generate_password_hash, check_password_hash

from Menagment.books.bookFactory import BookFactory
from books.book import *

class Librarians:
    def __init__(self, username, password, role):
        self.username = username
        self.password_hash = generate_password_hash(password)

    @staticmethod
    def let_borrow(book,username):
        if book.borrow_book(username):
            return True
        else:
            return False

    @staticmethod
    def return_book(title,author,username):
        loaned_books = pd.read_csv("loaned_books.csv")
        if username in loaned_books['username'].values and title in loaned_books['title'].values and author in loaned_books:

            # Increase the copies by 1
            available_books = pd.read_csv('available_books.csv')
            if title in available_books['title'].values and author in available_books['author'].values:
                available_books.loc[available_books['title'] == title, 'copies'] += 1
            else:
                available_books.append({
                'title': title,
                'author': author,
                'copies': 1
                }, ignore_index=True)

            # Remove the book from the loaned books CSV
            loaned_books = loaned_books.drop(
                loaned_books[(loaned_books['title'] == title) & (loaned_books['username'] == username) & (loaned_books['author'] == author)].index)

            # Save the updated available_books and loaned_books DataFrames back to the CSVs
            available_books.to_csv('available_books.csv', index=False)
            loaned_books.to_csv('loaned_books.csv', index=False)

            # Return a success message
            return True
        else:
            return False

    @staticmethod
    def add_book(book):
        books_df = pd.read_csv('books.csv')
        books_df = books_df.append(book.to_dict(), ignore_index=True)

        available_books = pd.read_csv('available_books.csv')
        available_books.append({
            'title': book.title,
            'author': book.author,
            'copies': book.copies
        }, ignore_index=True)

        books_df.to_csv('books.csv', index=False)
        available_books.to_csv('available_books.csv', index=False)
