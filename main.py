from GUI import *
import logging
import os
import csv

def ensure_csv_files():
    csv_files = {
        "books.csv": ["title", "author", "is_loaned", "copies", "genre", "year", "request", "available_copies", "queue"],
        "loaned_books.csv": ["title", "author", "year", "genre", "phone_number"],
        "users.csv": ["username", "password", "notification"]
    }

    for file_name, headers in csv_files.items():
        if not os.path.exists(file_name):
            with open(file_name, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
            print(f"Created {file_name} with headers: {', '.join(headers)}")

if __name__ == '__main__':
    logging.basicConfig(filename='library_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Ensure necessary CSV files exist
    ensure_csv_files()

    root = tk.Tk()
    app = GUI(root,logging)
    root.mainloop()