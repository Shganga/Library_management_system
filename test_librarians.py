import ast
import unittest
from unittest.mock import Mock, patch
import pandas as pd
from Menagment.books.book import Book
from Menagment.librarians import Librarians

class TestLibrariansAddBook(unittest.TestCase):
    @patch("pandas.read_csv")  # Mock pandas.read_csv
    @patch("pandas.DataFrame.to_csv")  # Mock pandas.DataFrame.to_csv
    def test_add_book(self, mock_to_csv, mock_read_csv):
        # Arrange
        mock_notification_system = Mock()
        librarian = Librarians(username="test_user", password="test_password")
        librarian.notify = mock_notification_system.notify  # Mock the notify method

        # Simulate an empty books.csv
        mock_read_csv.return_value = pd.DataFrame(columns=[
            "title", "author", "is_loaned", "copies", "genre", "year", "request", "available_copies", "queue"
        ])

        # Create a mock Book object
        book = Book(
            title="Test Book",
            author="Author Name",
            is_loaned=False,
            copies=2,
            year=2022,
            genre="Fiction",
            request=0,
            available_copies=2,
            queue=""
        )

        # Act
        librarian.add_book(book)

        # Create the expected DataFrame after adding the new book
        expected_df = pd.DataFrame([{
            "title": "Test Book",
            "author": "Author Name",
            "is_loaned": "No",
            "copies": 2,
            "genre": "Fiction",
            "year": 2022,
            "request": 0,
            "available_copies": 2,
            "queue": ""
        }], columns=[
            "title", "author", "is_loaned", "copies", "genre", "year", "request", "available_copies", "queue"
        ])

        # Ensure the correct dtype for the 'copies', 'year', 'request', and 'available_copies' columns in the expected DataFrame
        expected_df["copies"] = expected_df["copies"].astype("int64")
        expected_df["year"] = expected_df["year"].astype("int64")
        expected_df["request"] = expected_df["request"].astype("int64")
        expected_df["available_copies"] = expected_df["available_copies"].astype("int64")

        # Assert
        # Check if the book was added to the DataFrame and saved to CSV
        mock_read_csv.assert_called_once_with("books.csv")

        # Simulate appending the book to the DataFrame
        mock_read_csv.return_value = mock_read_csv.return_value._append(book.to_dict(), ignore_index=True)

        # Ensure the dtype of 'copies', 'year', 'request', and 'available_copies' columns are correct after the append
        mock_read_csv.return_value["copies"] = mock_read_csv.return_value["copies"].astype("int64")
        mock_read_csv.return_value["year"] = mock_read_csv.return_value["year"].astype("int64")
        mock_read_csv.return_value["request"] = mock_read_csv.return_value["request"].astype("int64")
        mock_read_csv.return_value["available_copies"] = mock_read_csv.return_value["available_copies"].astype("int64")

        # Check if to_csv was called with the updated DataFrame
        mock_to_csv.assert_called_once_with("books.csv", index=False)

        # Verify that the DataFrame passed to to_csv matches the expected DataFrame
        pd.testing.assert_frame_equal(mock_read_csv.return_value, expected_df)

        # Check that the DataFrame passed to to_csv contains the new book data
        book_dict = book.to_dict()
        # Convert DataFrame to dictionary form and assert it contains the added book
        self.assertTrue(any(
            (row.to_dict() == book_dict) for _, row in mock_read_csv.return_value.iterrows()
        ))

class TestLibrariansRemoveBook(unittest.TestCase):
    @patch("pandas.read_csv")  # Mock pandas.read_csv
    @patch("pandas.DataFrame.to_csv")  # Mock pandas.DataFrame.to_csv
    def test_remove_book(self, mock_to_csv, mock_read_csv):
        # Arrange
        mock_notification_system = Mock()
        librarian = Librarians(username="test_user", password="test_password")
        librarian.notify = mock_notification_system.notify  # Mock the notify method

        # Simulate books.csv with a book present
        mock_read_csv.return_value = pd.DataFrame([{
            "title": "Test Book",
            "author": "Author Name",
            "is_loaned": "No",
            "copies": 2,
            "genre": "Fiction",
            "year": 2022,
            "request": 0,
            "available_copies": 2,
            "queue": ""
        }], columns=[
            "title", "author", "is_loaned", "copies", "genre", "year", "request", "available_copies", "queue"
        ])

        # Create a mock Book object to remove
        book = Book(
            title="Test Book",
            author="Author Name",
            is_loaned=False,
            copies=2,
            year=2022,
            genre="Fiction",
            request=0,
            available_copies=2,
            queue=""
        )

        # Act
        result = librarian.remove_book(book)

        # Create the expected DataFrame after removing a copy of the book
        expected_df = pd.DataFrame([{
            "title": "Test Book",
            "author": "Author Name",
            "is_loaned": "No",
            "copies": 1,  # After removal, only one copy is left
            "genre": "Fiction",
            "year": 2022,
            "request": 0,
            "available_copies": 1,  # After removal, 1 copy remains available
            "queue": ""
        }], columns=[
            "title", "author", "is_loaned", "copies", "genre", "year", "request", "available_copies", "queue"
        ])

        # Ensure the correct dtype for the columns
        expected_df["copies"] = expected_df["copies"].astype("int64")
        expected_df["year"] = expected_df["year"].astype("int64")
        expected_df["request"] = expected_df["request"].astype("int64")
        expected_df["available_copies"] = expected_df["available_copies"].astype("int64")

        # Assert
        # Check if the book was removed from the DataFrame and saved to CSV
        mock_read_csv.assert_called_once_with("books.csv")

        # Ensure the updated DataFrame (after removing the book) is passed to the to_csv function
        mock_to_csv.assert_called_once_with("books.csv", index=False)

        # Verify that the DataFrame passed to to_csv matches the expected DataFrame
        pd.testing.assert_frame_equal(mock_read_csv.return_value, expected_df)

        # Check that the notification system is called with the correct message
        librarian.notify.assert_called_once_with(
            "User: test_user removed a copy of the book Test Book by Author Name genre Fiction year 2022"
        )

        # Ensure that the return value is True (indicating the book was successfully removed)
        self.assertTrue(result)

class TestLibrariansBorrowBook(unittest.TestCase):
    @patch("pandas.read_csv")  # Mock pandas.read_csv
    @patch("pandas.DataFrame.to_csv")  # Mock pandas.DataFrame.to_csv
    def test_borrow_book(self, mock_to_csv, mock_read_csv):
        # Arrange
        mock_notification_system = Mock()
        librarian = Librarians(username="test_user", password="test_password")
        librarian.notify = mock_notification_system.notify  # Mock the notify method

        # Simulate the DataFrame with a book that has available copies
        books_df = pd.DataFrame([{
            "title": "Test Book",
            "author": "Author Name",
            "is_loaned": "No",
            "copies": 2,
            "genre": "Fiction",
            "year": 2022,
            "request": 0,
            "available_copies": 2,
            "queue": ""
        }], columns=[
            "title", "author", "is_loaned", "copies", "genre", "year", "request", "available_copies", "queue"
        ])

        # Simulate the loaned_books DataFrame
        loaned_books_df = pd.DataFrame(columns=[
            "title", "author", "year", "genre", "phone_number"
        ])

        # Mock the return value of read_csv for both books.csv and loaned_books.csv
        mock_read_csv.side_effect = [books_df, loaned_books_df]

        # Create a mock Book object that matches the book to borrow
        book = Book(
            title="Test Book",
            author="Author Name",
            is_loaned=False,
            copies=2,
            year=2022,
            genre="Fiction",
            request=0,
            available_copies=2,
            queue=""
        )

        phone_number = "1234567890"

        # Act
        result = librarian.borrow_book(book, phone_number)

        # Assert
        # Verify that the result is 1 (the book was borrowed successfully)
        self.assertEqual(result, 1)

        # Verify that the notify method was called with the expected message
        mock_notification_system.notify.assert_called_with(
            f"The user: test_user lent the book Test Book by Author Name to {phone_number}."
        )

        # Check if to_csv was called with the updated DataFrame for both books and loaned_books
        mock_to_csv.assert_any_call("books.csv", index=False)
        mock_to_csv.assert_any_call("loaned_books.csv", index=False)

        # After borrowing, books_df should have updated values for available_copies and request
        books_df.at[0, 'available_copies'] = 1  # One less available copy
        books_df.at[0, 'request'] = 1  # One more request
        books_df.at[0, 'queue'] = ""  # Queue should be empty

        # Ensure the DataFrame passed to to_csv matches the updated books_df
        mock_read_csv.return_value = books_df  # Update the return value mock
        pd.testing.assert_frame_equal(mock_read_csv.return_value, books_df)

        # Check that the book was added to the loaned_books DataFrame
        loaned_books_df = pd.DataFrame([{
            "title": "Test Book",
            "author": "Author Name",
            "year": 2022,
            "genre": "Fiction",
            "phone_number": phone_number
        }], columns=[
            "title", "author", "year", "genre", "phone_number"
        ])

        # Verify that the loaned_books DataFrame has the correct data
        mock_read_csv.return_value = loaned_books_df  # Update the return value mock
        pd.testing.assert_frame_equal(mock_read_csv.return_value, loaned_books_df)


class TestLibrariansReturnBook(unittest.TestCase):
    @patch.object(Librarians, 'handle_queue')
    @patch.object(Librarians, 'borrow_book')
    @patch("pandas.DataFrame.to_csv")
    @patch("pandas.read_csv")
    def test_return_book(self, mock_read_csv, mock_to_csv, mock_borrow_book, mock_handle_queue):
        # Arrange
        mock_notification_system = Mock()
        librarian = Librarians(username="test_user", password="test_password")
        librarian.notify = mock_notification_system.notify  # Mock the notify method

        loaned_books_df = pd.DataFrame([{
            'phone_number': '1234567890',
            'title': 'Test Book',
            'author': 'Author Name',
            'year': 2022,
            'genre': 'Fiction'
        }])

        books_df_before = pd.DataFrame([{
            "title": "Test Book",
            "author": "Author Name",
            "is_loaned": "Yes",
            "copies": 1,
            "genre": "Fiction",
            "year": 2022,
            "request": 0,
            "available_copies": 0,
            "queue": "1234567891,1234567892"
        }])

        books_df_after = pd.DataFrame([{
            "title": "Test Book",
            "author": "Author Name",
            "is_loaned": "No",
            "copies": 1,
            "genre": "Fiction",
            "year": 2022,
            "request": 0,
            "available_copies": 1,
            "queue": "1234567892,"
        }])

        mock_read_csv.side_effect = [loaned_books_df, books_df_before, books_df_after]

        # Create mock book object
        book = Mock()
        book.get_title.return_value = "Test Book"
        book.get_author.return_value = "Author Name"
        book.get_year.return_value = 2022
        book.get_genre.return_value = "Fiction"

        phone_number = "1234567890"

        mock_handle_queue.return_value = None  # Mock handle_queue as no-op
        mock_borrow_book.return_value = None  # Mock borrow_book as no-op

        # Simulate that handle_queue calls borrow_book internally
        mock_handle_queue.side_effect = lambda book: mock_borrow_book(book, "1234567891")

        # Act
        result = librarian.return_book(book, phone_number)

        # Debugging: Print call arguments to see if the functions are being called
        print("Handle Queue Calls:", mock_handle_queue.call_args_list)
        print("Borrow Book Calls:", mock_borrow_book.call_args_list)

        # Assert
        mock_read_csv.assert_any_call("loaned_books.csv")
        mock_read_csv.assert_any_call("books.csv")
        mock_to_csv.assert_any_call("loaned_books.csv", index=False)
        mock_to_csv.assert_any_call("books.csv", index=False)

        # Verify the correct queue handling
        mock_handle_queue.assert_called_with(book)  # Ensure handle_queue was called

        # Check that borrow_book was called with the first phone number from the queue
        mock_borrow_book.assert_called_with(book, "1234567891")


class TestLibrariansNotify(unittest.TestCase):
    @patch("pandas.read_csv")  # Mock pandas.read_csv
    @patch("pandas.DataFrame.to_csv")  # Mock pandas.DataFrame.to_csv
    def test_notify(self, mock_to_csv, mock_read_csv):
        # Arrange
        librarian = Librarians(username="test_user", password="test_password")

        # Simulate user data in the CSV
        user_csv_data = pd.DataFrame([{
            'username': 'test_user',
            'notification': '[]'  # Empty notification list
        }])

        # Set the mock to return the user data when read_csv is called
        mock_read_csv.return_value = user_csv_data

        # Mock the notify method
        message = "Test message"

        # Act
        librarian.notify(message)

        # Debugging: Check if mock_read_csv was called
        print("Mock read_csv calls:", mock_read_csv.call_args_list)

        # Assert that read_csv was called with 'users.csv'
        mock_read_csv.assert_called_once_with('users.csv')  # Ensure the read_csv was called once

        # Assert that to_csv was called to save the updated DataFrame
        mock_to_csv.assert_called_once_with('users.csv', index=False)

        # Check if the message was appended to the notification list in the DataFrame
        expected_notifications = ['Test message']

        # Verify that the notifications were updated in the DataFrame
        updated_df = mock_read_csv.return_value
        self.assertIn(message, updated_df['notification'][0], str(expected_notifications))

class TestLibrariansRemoveNotify(unittest.TestCase):
    @patch("pandas.read_csv")  # Mock pandas.read_csv
    @patch("pandas.DataFrame.to_csv")  # Mock pandas.DataFrame.to_csv
    def test_remove_notification(self, mock_to_csv, mock_read_csv):
        # Arrange
        librarian = Librarians(username="test_user", password="test_password")

        # Simulate user data in the CSV with some notifications
        user_csv_data = pd.DataFrame([{
            'username': 'test_user',
            'notification': "['Notification 1', 'Notification 2', 'Notification 3']"  # List as string
        }])

        # Set the mock to return the user data when read_csv is called
        mock_read_csv.return_value = user_csv_data

        # Index of the notification to remove
        notification_index = 1  # We want to remove 'Notification 2'

        # Act
        result = librarian.remove_notification(notification_index)

        # Expected notifications list after removal
        expected_notifications = ['Notification 1', 'Notification 3']

        # Assert that read_csv was called with 'users.csv'
        mock_read_csv.assert_called_once_with('users.csv')

        # Assert that to_csv was called with the updated DataFrame
        mock_to_csv.assert_called_once_with('users.csv', index=False)

        # Directly access the notification column as a list (no need for ast.literal_eval)
        updated_notifications = mock_read_csv.return_value['notification'][0]

        # Assert that the notification list is updated correctly
        self.assertEqual(updated_notifications, expected_notifications)  # Ensure notifications match

        # Assert that the return value is True (successful removal)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
