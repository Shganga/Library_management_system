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





