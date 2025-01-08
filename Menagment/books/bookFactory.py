from Menagment.books.book import *

class BookFactory:
    @staticmethod
    def create_book(title, author, copies, year, genre):
        """Create a new book instance."""
        return Book(title, author, copies, year, genre)
