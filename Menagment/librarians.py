
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


    def borrow_book(self,title,author,phone_number):
        available_books = pd.read_csv('available_books.csv')
        if not available_books[(available_books['title'] == title) & (available_books['author'] == author)].empty:
            book_row = available_books.loc[(available_books['title'] == title) & (available_books['author'] == author)]
            if not book_row.empty :
                if book_row['copies'].values[0] > 0:
                    loaned_books = pd.read_csv("loaned_books.csv")
                    new_loan = {
                        'title': title,
                        'author': author,
                        'phone_number': phone_number
                    }
                    loaned_books = pd.concat([loaned_books, pd.DataFrame([new_loan])], ignore_index=True)
                    loaned_books.to_csv('loaned_books.csv', index=False)

                    available_books.loc[(available_books['title'] == title) & (available_books['author'] == author), 'copies'] -= 1
                    available_books.to_csv('available_books.csv', index=False)

                    books_csv = pd.read_csv('books.csv')
                    books_csv.loc[(books_csv['title'] == title) & (books_csv['author'] == author), 'requests'] += 1
                    if book_row['copies'].values[0] == 0:
                        books_csv.loc[(books_csv['title'] == title) & (books_csv['author'] == author), 'is_loaned'] = 'yes'
                    books_csv.to_csv('books.csv', index=False)

                else:
                    print('No loaned books available')



    def return_book(self,title,author, phone_number):
        loaned_books = pd.read_csv("loaned_books.csv")
        if not loaned_books[(loaned_books['phone_number'] == phone_number) & (loaned_books['title'] == title) & (loaned_books['author'] == author)].empty:

            # Increase the copies by 1
            available_books = pd.read_csv('available_books.csv')
            if not available_books[(available_books['title'] == title) & (available_books['author'] == author)].empty:
                available_books.loc[available_books['title'] == title, available_books['author'] == author ,'copies'] += 1
            else:
                "no such book"
            # else:
            #     available_books.append({
            #     'title': title,
            #     'author': author,
            #     'copies': 1
            #     }, ignore_index=True)
            #
            # Remove the book from the loaned books CSV
            loaned_books = loaned_books.drop(
                loaned_books[(loaned_books['title'] == title) & (loaned_books['phone_number'] == phone_number) & (loaned_books['author'] == author)].index)

            # Save the updated available_books and loaned_books DataFrames back to the CSVs
            available_books.to_csv('available_books.csv', index=False)
            loaned_books.to_csv('loaned_books.csv', index=False)

            # Return a success message
            return True
        else:
            return False


    def add_book(self,book):
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

    def remove_book(self,book):
        books_df = pd.read_csv('books.csv')
