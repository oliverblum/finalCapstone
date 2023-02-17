"""
This is a program that can be used by a bookstore clerk to:
- add new books to the database
- update book information
- delete books from the database
- search the database to find a specific book.

Database is of the following form:

id	    Title	                                  Author	       Qty
3001	A Tale of Two Cities	                  Charles Dickens  30
3002	Harry Potter and the Philosopher's Stone  J.K. Rowling     40
3003	The Lion the Witch and the Wardrobe	      C. S. Lewis      25
3004	The Lord of the Rings J.R.R Tolkien	      J.R.R Tolkien    37
3005	Alice in Wonderland	                      Lewis Carroll	   12
"""

###################
#     Modules     #
###################
# make sure you have the tabulate library installed by doing the following:
# - Type CMD in the search bar and open the Command Prompt application.
# - Type "pip install tabulate --user" and press Enter
# if installation does not work, follow steps in https://www.youtube.com/watch?v=I6-_W-SuSG4
from tabulate import tabulate

# SQLite (part of standard library)
import sqlite3

###################
#    Functions    #
###################
def print_cursor(my_message = ""):
    """
    Function prints out first 10 books in the books table
    """
    print(f"\n^^^^  {my_message} \n")

    # select all books in db
    cursor.execute('''SELECT * FROM books''')

    # stack first 10 books in a list
    results = []
    for i, row in enumerate(cursor):
        if i <= 10:
            results.append([row[0], row[1], row[2], row[3]])

    # print out list using tabulate
    print(tabulate(results, headers=["id", "Title", "Author", "Qty"]))
    return results

def enter_book():
    """
    Function allows user to enter a new book to the data base
    """
    print("^^^^ Provide details of new book to add to data base ^^^^")
    # user inputs ID
    id = None
    while id is None:
        try:
            id = int(input("ID:       ").strip())
        except ValueError:
            print(f"ID has to be an integer. Try again.")

    # User inputs title and author
    title   = str(input("Title:    "))
    author  = str(input("Author:   "))
    
    # user inputs quantity
    qty = None
    while qty is None:
        try:
            qty     = int(input("Quantity: "))
        except ValueError:
            print(f"Quantity has to be an integer. Try again.")

    # write to data base
    cursor.execute('''INSERT INTO books(id, Title, Author, Qty) VALUES(?,?,?,?)''', (id,title,author,qty))
    db.commit()

    # test
    print_cursor(f"inserted ID {id} into data base:")
    return

def id_exists(id):
    """
    Function looks up an ID in the database and returns TRUE if it exists and FALSE otherwise
    """
    try:
        # search data base for ID
        cursor.execute('''SELECT id FROM books WHERE id = ?''', (id,))
        
        # if id matches id found, returns TRUE
        if id == cursor.fetchone()[0]:
            return True

    except TypeError:
        return False

def field_update(id, field, field_value):
    """
    Function updates a given field for book with ID provided
    """
    cursor.execute(f'''UPDATE books SET {field} = ? WHERE id = ? ''', (field_value, id))
    db.commit()
    return

def update_book():
    """
    Function allows user to update a book in the data base
    """
    # user inputs ID to update
    id = None
    while id is None:
        try:
            id = int(input("^^^^ Provide ID you want to update ^^^^\nID: ").strip())
        except ValueError:
            print(f"ID has to be an integer. Try again.")
    
    if id_exists(id) == False:
        print(f"Error: ID {id} not found in data base.")
        return
    else:
        # what Field does user want to update?
        selection = input(f"""
^^^^ id {id}: Select Field to Update ^^^^
1   Title
2   Author
3   Quantity
0   Exit

Selction: 
"""     ).lower().strip()

        # selection mapping to field
        if selection   == "1": field = "Title"
        elif selection == "2": field = "Author"
        elif selection == "3": field = "Qty"
        elif selection == "0":
            return
        else:
            print("Error: invalid selection")
            return

        new_value = input(f"""^^^^ id {id}: update {field} ^^^^\nInput: """ ).lower().strip()

        # update field
        field_update(id, field, new_value)

        # test
        print_cursor(f"ID {id}: updated {field} to {new_value}.")
        return

def delete_book():
    """
    This function deletes a book with the provided ID from the data base
    """
    # ask user for ID to delete
    id = None
    while id is None:
        try:
            id = int(input("""^^^^ Provide ID you want to delete ^^^^\nID: """).strip())
        except ValueError:
            print(f"ID has to be an integer. Try again.")
    
    if id_exists(id) == False:
        print(f"Error: ID {id} not found in data base.")
        return
    else:
        # delete ID from db
        cursor.execute('''DELETE FROM books WHERE id = ? ''', (id,))
        db.commit()

        # test
        print_cursor(f"ID {id}: deleted.")
        return

def search_book():
    """
    This function looks up a book with a provided ID from the data base
    """
    # ask user for ID to look up
    id = None
    while id is None:
        try:
            id = int(input("""^^^^ Provide ID you want to look up ^^^^\nID: """).strip())
        except ValueError:
            print(f"ID has to be an integer. Try again.")

    if id_exists(id) == False:
        print(f"Error: ID {id} not found in data base.")
        return
    else:
        # return all fields and stack cursor results into list
        cursor.execute('''SELECT * FROM books WHERE id = ?''', (id,))
        results = []
        for row in cursor:
                results.append([row[0], row[1], row[2], row[3]])

        # print list using tabulate
        print(tabulate(results, headers=["id", "Title", "Author", "Qty"]))
        return

###################
#     Program     #
###################
try: 
    # === Create a database called ebookstore ===
    db = sqlite3.connect("ebookstore.db")
    cursor = db.cursor()

    # create the table called books 
    cursor.execute('''CREATE TABLE books
                  (id real, Title text, Author text, Qty real)''')

    # commit changes (remember the commit function is invoked on the db object)	
    db.commit()

    # === Inserts the following new books into the table ===
    """
id	    Title	                                  Author	       Qty
3001	A Tale of Two Cities	                  Charles Dickens  30
3002	Harry Potter and the Philosopher's Stone  J.K. Rowling     40
3003	The Lion the Witch and the Wardrobe	      C. S. Lewis      25
3004	The Lord of the Rings J.R.R Tolkien	      J.R.R Tolkien    37
3005	Alice in Wonderland	                      Lewis Carroll	   12
    """
    books = [
            (3001,"A Tale of Two Cities","Charles Dickens",30),
            (3002,"Harry Potter and the Philosopher's Stone","J.K. Rowling",40),
            (3003,"The Lion the Witch and the Wardrobe","C. S. Lewis",25),
            (3004,"The Lord of the Rings J.R.R Tolkien","J.R.R Tolkien",37),
            (3005,"Alice in Wonderland","Lewis Carroll",12)
            ]
    cursor.executemany('''INSERT INTO books(id, Title, Author, Qty) VALUES(?,?,?,?)''', books)
    db.commit()

except:
    # if table already exists, just connect to db
    db = sqlite3.connect("ebookstore.db")
    cursor = db.cursor()

finally:
    while True:
        # user selection menu
        user_selection = input("""
^^^^ Select Option ^^^^
1   Enter book
2   Update book
3   Delete book
4   Search books
0   Exit

Selction: 
"""
        ).lower().strip()

        if user_selection   == "1":
            enter_book()
        elif user_selection == "2":
            update_book()
        elif user_selection == "3":
            delete_book()
        elif user_selection == "4":
            search_book()
        elif user_selection == "0":
            # When done working with the db, need to close the connection
            cursor.close()

            # Exit
            print('Goodbye!!!')
            exit()

        else:
            print("Try again. Select one of the provided options.")
