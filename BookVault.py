import sqlite3
import os

# Make sure that we're working in the correct
# directory before creating the database.
python_file_directory = os.path.dirname(os.path.abspath(__file__))
if os.getcwd() != python_file_directory:
    os.chdir(python_file_directory)


# Book class.
# I'm not sure if I should use a class as it seems unnecessary.
# I added it as the task says we should use all that we have learnt so far.
class Book:
    """A class that represents a book in the database.

    Attributes:
        id (int) = Unique identifier per book
        title (string) = Title of book
        author (string) = Author of book
        qty (int) = Quantity of this book in stock
    """

    def __init__(self, details):
        """Initializes an instance of a book

        Parameters:
            id (int) = Unique identifier per book
            title (string) = Title of book
            author (string) = Author of book
            qty (int) = Quantity of this book in stock
        """
        self.id = details[0]
        self.title = details[1]
        self.author = details[2]
        self.qty = details[3]

    def delete(self, cursor):
        """This method deletes the specific book.

        Parameters:
            cursor(db.cursor) = SQLite3 database cursor
        """

        print(
            f"""
The following book will be deleted:
ID: {self.id}
Title: {self.title}
Author: {self.author}
        """
        )
        if confirm(input("\nDelete book from database? (Y/N)\n")):
            cursor.execute(
                "DELETE FROM book WHERE id = ?",
                (self.id,),
            )
            print("\nBook successfully deleted!\n")
        else:
            print("\nOperation cancelled.\n")

    def update(self, cursor):
        """This method updates the selected book in the database

        Parameters:
            cursor(db.cursor) = SQLite3 database cursor
        """

        print(
            f"""
Selected book:
ID: {self.id}
Title: {self.title}
Author: {self.author}
Quantity: {self.qty}"""
        )

        answer = input(
            """
What would you like to update?
1. Title
2. Author
3. Quantity
4. Cancel

:"""
        )
        # Capture updated details
        updated_details = [self.id, self.title, self.author, self.qty]
        while True:
            if answer == "1":
                updated_details[1] = input("\nNew title:\n")
            elif answer == "2":
                updated_details[2] = input("\nNew author:\n")
            elif answer == "3":
                updated_details[3] = input("\nNew quantity:\n")
            elif answer == "4":
                print("\nOperation cancelled.\n")
                break
            else:
                print("\nPlease enter a valid option.\n")

            if verify_details(updated_details):
                # Swap first and last values
                updated_details.append(updated_details.pop(0))

                cursor.execute(
                    """UPDATE book
    SET title = ?, author = ?, qty = ?
    WHERE id = ?;""",
                    updated_details,
                )
                self.title = updated_details[1]
                self.author = updated_details[2]
                self.qty = updated_details[3]
                db.commit()
                print("\nBook updated successfully!\n")
                break


# Add book to DB
def add_book():
    """This function adds a book to the database.
    It prompts the user to enter the new details of the book
    then sends a SQL query to add it to the database."""

    while True:
        new_book = []
        new_book.append(generate_new_id())
        new_book.append(input("\nEnter the new book's title:\n").strip())
        new_book.append(input("\nEnter the new book's author:\n").strip())
        new_book.append(input("\nEnter the quantity:\n").strip())

        if verify_details(new_book):
            print(
                f"\nConfirm details:\n"
                f"\nID: {new_book[0]}\n"
                f"Title: {new_book[1]}\n"
                f"Author: {new_book[2]}\n"
                f"Quantity: {new_book[3]}\n"
            )

            if confirm(input("Add book to database? (Y/N)\n")):
                cursor.execute(
                    """INSERT INTO book (id,title,author,qty)
                    VALUES (?,?,?,?);""",
                    new_book,
                )
                db.commit()
                print("\nBook added successfully!\n")
            else:
                print("\nOperation cancelled.\n")
                break

            if confirm(input("Add another book? (Y/N)\n")):
                continue
            else:
                break


# Verify data before writing to DB
def verify_details(book_details):
    """This function is used to verify a books details
    before trying to add it to the database ensuring
    data entegrity.
    ID needs to be an integer
    Author cannot be empty
    Title cannot be empty
    Quantity cannot be negative and must be an integer.

    Parameters:
        book_details (list) = A list containing the details
            of the book that needs to be added to the database:
            [id (int), title (string), author (string), qty (int)]

    Returns:
        False if any of the above conditions aren't met
        True if the data is in the correct format

    """
    try:
        book_id = int(book_details[0])
        qty = int(book_details[3])
    except ValueError:
        print("\nID and Quantity must be numbers.")
        return False

    if book_id <= 0 or qty <= 0:
        print("\nID and Quantity must be positive.")
        return False

    if not book_details[1].strip() or not book_details[2].strip():
        print("\nTitle and Author cannot be empty.")
        return False

    return True


# Search for books
def search_books(details=list):
    """This function uses dynamic search to build a SQL query to search for
    books in the database. It takes a list of search criteria and prints
    the results to the user.

    Parameters:
        details (list) = A list of details the user wants to search for.
            [id (int), title (string), author (string), qty (int)]

    Returns:
        input = Asking the user if they want to search again.
            "Y" calls the function again
            "N" exits the function.
    """

    # 1=1 always true so use this as first statement and
    # append "AND" to other values
    # https://pushmetrics.io/blog/why-use-where-1-1-in-sql-
    # queries-exploring-the-surprising-benefits-of-a-seeming
    # ly-redundant-clause/#:~:text=What%20Does%20"WHERE%201%
    # 3D1,not%20filter%20out%20any%20records.

    query = "SELECT * FROM book WHERE 1=1"
    parameters = []

    if details[0] != "":
        query += " AND id = ?"
        parameters.append(f"%{details[0]}%")

    if details[1] != "":
        query += " AND title LIKE ?"
        parameters.append(f"%{details[1]}%")

    if details[2] != "":
        query += " AND author LIKE ?"
        parameters.append(f"%{details[2]}%")

    if details[3] != "":
        try:
            qty_int = int(details[3])
            query += " AND qty = ?"
            parameters.append(f"{qty_int}")
        except ValueError:
            print("Quantity invalid. Make sure it's a number.")

    cursor.execute(query, parameters)
    results = cursor.fetchall()
    if len(results) == 0:
        print("\n===X No books found X===\n")
        print("Verify search details.")
    else:
        print("\n==== Results: ====")
        for row in results:
            print(f"\nID: {row[0]}")
            print(f"Title: {row[1]}")
            print(f"Author: {row[2]}")
            print(f"Quantity: {row[3]}\n")
            print("-" * 50)

    return confirm(input("\nSearch again? Y/N\n"))


# Extra function to list all books in DB
def list_all():
    """This function lists all books in the database by printing
    the results in the output window.
    """
    cursor.execute("""SELECT * FROM book ORDER BY id ASC;""")
    results = cursor.fetchall()

    if len(results) == 0:
        print("\n===X No books found X===\n")
        print("Add a book using option 1.")
    else:
        print("\n==== All books: ====")
        for row in results:
            print(f"\nID: {row[0]}")
            print(f"Title: {row[1]}")
            print(f"Author: {row[2]}")
            print(f"Quantity: {row[3]}\n")
            print("-" * 50)


# Generate a unique ID for each new book
def generate_new_id():
    """This function generates a unique ID for each book based on the
    last entry to the database."""
    # ID's only need to be unique so no need to search through the
    # entire database just to find a missing number. i.e.
    # if 3002 doesn't exist, an added book will not have the ID 3002.
    # It will have the ID incremented by one from the MAX number found
    # in the column.
    # (I think the code makes more sense than the explanation above)
    cursor.execute("""SELECT MAX(id) FROM book;""")
    last_id = cursor.fetchone()[0]
    if last_id is not None:
        new_id = int(last_id + 1)
    else:
        # For incase there are no entries yet
        new_id = 3000
    return new_id


# Small function to confirm "Yes/No" answers
def confirm(answer=str):
    """A small function to confirm a yes or no input."""
    answer = answer.lower().strip()
    # Preventing endless loop with retry limit.
    retries = 3
    while retries > 0:
        if answer == "y":
            return True
        elif answer == "n":
            return False
        else:
            answer = input("\nPlease enter Y (Yes) or N (No).\n").lower()
        retries -= 1
    print("Too many invalid entries. Defaulting to No.")
    return False


# Load users into dictionary.
def load_users():
    try:
        with open("users.txt", "r", encoding="utf-8") as user_document:
            user_dictionary = {}

            for line in user_document:
                user_details = line.split(", ")
                user_name = user_details[0]
                user_password = user_details[1].strip()
                user_dictionary.update({user_name: user_password})
        return user_dictionary

    except FileNotFoundError:
        return print(
            "Please make sure the user.txt file is in the same directory as "
            "the currently running python file."
        )


def login():
    """This function serves as the login confirmation.
    It will only allow a user to continue if a valid and matching
    username and password is given.
    """
    # Login prompt
    user_dictionary = load_users()

    if user_dictionary == {}:
        exit()

    retries = 0
    retry_max = 3
    while True:
        login_username = input("\nUsername: ")

        # Check username
        if login_username in user_dictionary and retries <= retry_max:
            login_password = input("Password: ")

            # Check password
            if login_password == user_dictionary.get(login_username):
                print(f"\nWelcome {login_username.capitalize()}!\n")
                return True
            else:
                print(
                    "\nPassword incorrect. Try again.\n"
                    f"Retries remaining {retry_max-retries}"
                )
                retries += 1
                continue
        elif retries <= retry_max:
            print(
                f"\nUser {login_username} is not registered. "
                "Please enter a valid username.\n"
                f"Retries remaining {retry_max-retries}"
            )
            retries += 1
            continue
        else:
            print("\nRetry limit reached!")
            return False


# region DB creation

db = sqlite3.connect("ebookstore.db")
cursor = db.cursor()

# ====== RESET/DELETE TABLE FOR TESTING ONLY! ======
# cursor.execute("""DROP TABLE IF EXISTS book;""")


# Check if table exists:
# https://www.geeksforgeeks.org/check-if-table-exists-in-sqlite-using-python/

table_list = cursor.execute(
    """SELECT * FROM sqlite_master
    WHERE type='table';"""
).fetchall()

if table_list == []:
    print("Table does not exist. Creating table with default values...")
    cursor.execute(
        """CREATE TABLE book (
        id INT PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        qty INT NOT NULL
        );"""
    )

    row_data = [
        (3001, "A Tale of Two Cities", "Charles Dickens", 30),
        (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
        (3003, "The Lion, the Witch and the Wardrobe", "C. S. Lewis", 25),
        (3004, "The Lord of the Rings", "J.R.R. Tolkien", 37),
        (3005, "Alice in Wonderland", "Lewis Carrol", 12),
        (3006, "The Anxious Generation", "Jonathon Haidt", 15),
        (3007, "Onyx Storm", "Rebecca Yarros", 12),
        (3008, "The Great Gatsby", "F. Scott Fitzgerald", 40),
        (3009, "1984", "George Orwell", 25),
        (3010, "The Girl with the Dragon Tattoo", "Stieg Larsson", 35),
        (3011, "Ender's Game", "Orson Scott Card", 32),
    ]

    cursor.executemany(
        """INSERT INTO book
                VALUES (?,?,?,?);""",
        row_data,
    )
    db.commit()
    print("Table created.")

else:
    print("Table already exists. Continuing.")

# endregion


# Welcome menu
print(
    """
-------------------------
Welcome to the Book DB!
-------------------------

Please log in:
"""
)


if login():
    while True:
        option = (
            input(
                """
    === Main Menu ===

    Please choose an option:
    1. Add book
    2. Update book
    3. Delete book
    4. Search books
    5. List all books
    0. Exit

    :"""
            )
            .lower()
            .strip()
        )

        # Add Book Option
        if option == "1":
            add_book()

        # Update Book Option
        elif option == "2":
            while True:
                try:
                    update_book_id = int(input("\nBook ID to update:\n"))
                    cursor.execute(
                        """SELECT * FROM book WHERE id = ?;""", (update_book_id,)
                    )
                    book_details = cursor.fetchone()
                    if book_details is not None:
                        book = Book(book_details)
                        book.update(cursor)
                        if confirm(input("Update another value? (Y/N)")):
                            continue
                        else:
                            break
                    else:
                        print(f"\nUnable to locate book with ID: {update_book_id}")
                        print(
                            """Please insert a valid ID.
    Use Option 5 to list or Option 4 to search for the book and
    find it's appropriate ID.
                    """
                        )

                except ValueError:
                    print(
                        """Please insert a valid ID.
    Make sure that it only consists of numbers.
    Use Option 5 to list or Option 4 to search for the book and
    find it's appropriate ID.
                    """
                    )

                if confirm(input("\nTry again? Y/N\n")):
                    continue
                else:
                    break

        # Delete Book Option
        elif option == "3":
            while True:
                try:
                    delete_book_id = int(input("\nBook ID to delete:\n"))
                    cursor.execute(
                        """SELECT * FROM book WHERE id = ?;""", (delete_book_id,)
                    )
                    book_details = cursor.fetchone()
                    if book_details is not None:
                        book = Book(book_details)
                        book.delete(cursor)
                        db.commit()
                        break
                    else:
                        print(f"\nUnable to locate book with ID: {delete_book_id}")
                        print(
                            """
    Use Option 5 to list or Option 4 to search for the book and
    find it's appropriate ID.
                    """
                        )

                except ValueError:
                    print(
                        """Please insert a valid ID that only conists of numbers.
    Use Option 5 to list or Option 4 to search for the book and
    find it's appropriate ID.
                    """
                    )

                if confirm(input("\nTry again? Y/N\n")):
                    continue
                else:
                    break

        # Search for Book Option
        elif option == "4":
            print(
                """
                ====== SEARCH =====
    Please enter the following details of the book.
    Blank and partial values are accepted."""
            )
            while True:
                search_details = []
                search_details.append(input("\nID: "))
                search_details.append(input("Title: "))
                search_details.append(input("Author: "))
                search_details.append(input("Quantity: "))

                if search_books(search_details):
                    continue
                else:
                    break

        # List Books Option
        elif option == "5":
            list_all()

        # Exit Option
        elif option == "0":
            print(
                """
    Thank you for using the Book DB!
    Happy reading!

    Program exiting...
    """
            )
            db.close()
            exit()
        else:
            print("\nPlease enter a valid option!\n")

else:
    print("Invalid login. Program exiting...")
    db.close()
    exit()
