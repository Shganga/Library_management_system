import pandas as pd

class Book:
    def __init__(self, title, author, is_loaned ,copies, year, genre, request ,available_copies):
        self.__title = title
        self.__author = author
        self.__is_loaned = is_loaned
        self.__copies = copies
        self.__year = year
        self.__genre = genre
        self.__request = request
        self.__available_copies = available_copies

    def to_dict(self):
        """Converts the instance to a dictionary."""
        return {
            'title': self.__title,
            'author': self.__author,
            'is_loaned': self.__is_loaned,
            'copies': self.__copies,
            'genre': self.__genre,
            'year': self.__year,
            'requests': self.__request,
            'available_copies': self.__available_copies
        }

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_is_loaned(self):
        return self.__is_loaned

    def get_copies(self):
        return self.__copies

    def get_year(self):
        return self.__year

    def get_genre(self):
        return self.__genre

    def get_request(self):
        return self.__request

    def get_available_copies(self):
        return self.__available_copies





