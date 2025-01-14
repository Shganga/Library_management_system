# Library management system 


## Instructions for running the project

Press the run button and wait for the window to open, after it opens you will see a page with alot of library actions such as 
adding a book lending a book and so on. To accesses these pages first you will need to login (top right corner)and if you dont have an account you will have to register
(pressing the buttons without logging in will create a popup window that reminds you to log in to have permission).
after you logged in you cna access all the pages and the notification for your account.

## Description of the system features

Our system supports basic action that a librarian can do in the library system. <br>

Add book: a librarian can add a book to the library, after pressing the add book button he will be taken to a page with 5 fields: title,author,copies,year,genre. The librarian will fill these fields and add the book, if the book already exists it will add the new copies to the current ones if he doesn't he will be added as a new book in the library. <br>

Remove book: a librarian can remove a copy of a book from the library, after pressing the remove book button he will be taken to a page with a listbox (a list that allows us to choose a line) of all the books in the library, as long as the field is_loaned is not 'yes' the librarian can remove a copy of the book if the field is 'yes' it means that there are no copies at the library so he cant remove it from the system, and he has to wait until a copy is returned.(if the librarian removes a copy and the copies field = 0 the book will be erased from the library database)

View books: a librarian can look at all the books in the library and additionally he can look for a specific or a group of them, He/She can filter by author, title, genre, and available books (author,title,genre are all search with partial matching and the list dynamic changes so the librarian has an easier time).<br>

Lend book: a librarian can lend a book to a customer, after pressing the lend book button he will be taken to a page with list of all the books, after choosing a book and entering the customers phone number he/she can lend the book by pressing the borrow button(it will add +1 to the request field of the book). The info of the book and the phone number will be saved in a csv file named loaned_books, if all the copies of this book are loaned the customer will be added to the waiting list and when the book becomes available it will send a notification and lend him the book.

Return book: a librarian needs to return the book in the system after the customer brought it back so it can be loaned, the librarian will choose the book that has the phone number of the customer from the list of loaned books and return it.

Popular books: a librarian can see the top 10 most requested books in the library

Logout: In the top right corner there is an option to logout

Notifications: In the top right corner there is a picture of a text buble pressing it will take the librarian to a page that shows him his notifications he can keep them or select which he wants to delete(if a librarian deletes a notification it will be deleted only for him).

HomePage: In the top left there is a picture of a house this button takes the current librarian back to the main page.

## Design patterns that were implemented

### Factory, Observer, Strategy, Decorator


