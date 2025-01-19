# Library Management System

## Instructions for Running the Project

1. Press the **Run** button from the main.py file and wait for the application window to open.
2. Once the window opens, you will see a homepage displaying various library actions, such as adding a book, lending a book, and more.
3. To access these features, you must first log in by clicking the **Login** button in the top-right corner.
   - If you do not have an account, you will need to register.
   - Attempting to use the system without logging in will trigger a popup reminding you to log in to gain the necessary permissions.
4. After logging in, you can access all the features and view notifications related to your account.

## System Features

### Add Book
- **Functionality:** Librarians can add books to the library database.
- **Process:**
  1. Click the **Add Book** button to navigate to the book addition page.
  2. Fill in the following fields:
     - Title
     - Author
     - Number of Copies
     - Year
     - Genre
  3. If the book already exists, the entered number of copies will be added to the existing count. If it does not exist, a new entry will be created in the database.

### Remove Book
- **Functionality:** Librarians can remove copies of a book from the library.
- **Process:**
  1. Click the **Remove Book** button to navigate to the removal page.
  2. Select a book from the list of library books.
  3. Copies can only be removed if the book is not currently loaned out (i.e., the "is_loaned" field must be "no").
  4. If all copies of a book are removed (i.e., the number of copies becomes zero), the book is permanently deleted from the library database.

### View Books
- **Functionality:** Librarians can view all books / available books / loaned books in the library and search through them.
- **Features:**
  - Search by:
    - Author
    - Title
    - Genre
    - Availability
  - Partial matching is supported.

### Lend Book
- **Functionality:** Librarians can lend books to customers.
- **Process:**
  1. Click the **Lend Book** button to view a list of all available books.
  2. Select a book and enter the customer's phone number.
  3. Click the **Borrow** button to complete the lending process.
     - The request count for the book is incremented.
     - The book and customer information are recorded in a CSV file named `loaned_books`.
     - If all copies of the book are loaned out, the customer is added to a waiting list.
  4. When the book becomes available, the system sends a notification and automatically lends the book to the customer.

### Return Book
- **Functionality:** Librarians can return books that have been loaned out.
- **Process:**
  1. Select the book and the customer's phone number from the list of loaned books.
  2. Click the **Return** button to update the system.

### Popular Books
- **Functionality:** View the top 10 most requested books in the library.

### Notifications
- **Functionality:** Librarians can view and manage notifications.
- **Process:**
  1. Click the notification icon (text bubble) in the top-right corner.
  2. Notifications can be reviewed and individually deleted. Deleting a notification only removes it for the logged-in librarian.

### Logout
- **Functionality:** Logout of the system by clicking the **Logout** button in the top-right corner.

### Homepage
- **Functionality:** Return to the main page by clicking the **Home** icon (house) in the top-left corner.

## Design Patterns Implemented

### Factory Pattern
- Used for creating instances of different classes in the system, ensuring flexibility and reusability.

### Observer Pattern
- Implemented for the notification system to inform librarians of updates, such as when a book becomes available.

### Strategy Pattern
- Applied to the search and filtering functionality, allowing dynamic changes to the filtering criteria without altering the core logic.

### Decorator Pattern
- Used to enhance existing functionalities, such as extending book attributes or adding additional logging features without modifying the original code.

---
This system provides a streamlined and efficient way to manage library operations while maintaining a user-friendly interface for librarians.

