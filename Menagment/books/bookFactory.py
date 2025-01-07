from book import *

class BookFactory:
    def __init__(self, books_csv='books.csv'):
        self.books_csv = books_csv
        self._initialize_file()

    def _initialize_file(self):
        """Ensure the CSV file exists and create it if necessary."""
        try:
            pd.read_csv(self.books_csv)
        except FileNotFoundError:
            # If the file doesn't exist, create it with default columns
            pd.DataFrame(columns=["title", "author", "is_loaned" , "copies", "genre", "year" , "request" ]).to_csv(self.books_csv, index=False)

    @staticmethod
    def create_book(title, author, copies, year, genre):
        """Create a new book instance."""
        return Book(title, author, copies, year, genre)

    def save_book(self, book):
        """Save a Book instance to the CSV file."""
        book_dict = book.to_dict()
        books_df = pd.read_csv(self.books_csv)
        books_df = books_df.append(book_dict, ignore_index=True)
        books_df.to_csv(self.books_csv, index=False)

    def get_book_by_title(self, title):
        """Retrieve a book by its title from the CSV file."""
        books_df = pd.read_csv(self.books_csv)
        book_row = books_df[books_df['title'] == title]
        if not book_row.empty:
            return Book(book_row['title'].values[0],
                        book_row['author'].values[0],
                        book_row['is_loaned'].values[0],
                        book_row['copies'].values[0],
                        book_row['year'].values[0],
                        book_row['genre'].values[0])
        return None  # If no book with that title exists

    def update_book(self, title, **kwargs):
        """Update a book's details in the CSV file based on its title."""
        books_df = pd.read_csv(self.books_csv)
        if title in books_df['title'].values:
            for key, value in kwargs.items():
                if key in books_df.columns:
                    books_df.loc[books_df['title'] == title, key] = value
            books_df.to_csv(self.books_csv, index=False)
        else:
            raise ValueError(f"Book with title '{title}' not found.")

    def delete_book(self, title):
        """Delete a book from the CSV file based on its title."""
        books_df = pd.read_csv(self.books_csv)
        if title in books_df['title'].values:
            books_df = books_df[books_df['title'] != title]
            books_df.to_csv(self.books_csv, index=False)
        else:
            raise ValueError(f"Book with title '{title}' not found.")