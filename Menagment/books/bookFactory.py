from Menagment.books.book import *

class BookFactory:
    @staticmethod
    def create_book(title, author, is_loaned ,copies, year, genre, request ,available_copies):
        """Create a new book instance."""
        return Book(title, author, is_loaned ,copies, year, genre, request ,available_copies)
