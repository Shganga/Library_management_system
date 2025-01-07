import pandas as pd

class Book:
    def __init__(self, title, author, copies, year, genre):
        self.__title = title
        self.__author = author
        self.__is_loaned = False
        self.__copies = copies
        self.__year = year
        self.__genre = genre

    def to_dict(self):
        """Converts the instance to a dictionary."""
        return {
            'title': self.__title,
            'author': self.__author,
            'is_loaned': self.__is_loaned,
            'copies': self.__copies,
            'genre': self.__genre,
            'year': self.__year,
            'requests': 0  # Add 'requests' with initial value 0
        }

    def borrow_book(self, username):
        # Read the available books CSV into a DataFrame
        available_books = pd.read_csv('available_books.csv')

        # Check if the book exists in the DataFrame
        if self.__title in available_books['title'].values:
            # Get the row where the title matches
            book_row = available_books[available_books['title'] == self.__title].iloc[0]

            # Reduce the copies by 1
            available_books.loc[available_books['title'] == self.__title, 'copies'] -= 1

            # Add the borrowed book details (title, author, username) to loaned_books.csv
            loaned_books = pd.read_csv('loaned_books.csv')
            loaned_books = loaned_books.append({
                'title': self.__title,
                'author': self.__author,
                'username': username
            }, ignore_index=True)
            loaned_books.to_csv('loaned_books.csv', index=False)

            # Check if copies have reached 0
            if available_books.loc[available_books['title'] == self.__title, 'copies'].values[0] == 0:
                available_books = available_books[available_books['title'] != self.__title]

            # Save the updated available_books DataFrame back to the CSV
            available_books.to_csv('available_books.csv', index=False)

            books_csv = pd.read_csv('books.csv')
            books_csv.loc[books_csv['title'] == self.__title, 'requests'] += 1
            books_csv.to_csv('books.csv', index=False)
            # Return a success message
            return True
        else:
            return False

    def return_book(self,username):
        loaned_books = pd.read_csv('loaned_books.csv')

        # Check if the book exists in the loaned books CSV and matches the username
        if username in loaned_books['username'].values and self.__title in loaned_books['title'].values:
            # Get the row where the title and username match
            borrowed_book = loaned_books[(loaned_books['title'] == self.__title) & (loaned_books['username'] == username)].iloc[0]

            # Increase the copies by 1
            available_books = pd.read_csv('available_books.csv')
            if self.__title in available_books['title'].values and self.__author in available_books['author'].values:
                available_books.loc[available_books['title'] == self.__title, 'copies'] += 1
            else:
                available_books.append({
                'title': self.__title,
                'author': self.__author,
                'copies': 1
                }, ignore_index=True)


            # Remove the book from the loaned books CSV
            loaned_books = loaned_books.drop(
                loaned_books[(loaned_books['title'] == self.__title) & (loaned_books['username'] == username)].index)

            # Save the updated available_books and loaned_books DataFrames back to the CSVs
            available_books.to_csv('available_books.csv', index=False)
            loaned_books.to_csv('loaned_books.csv', index=False)

            # Return a success message
            return True
        else:
            return False



