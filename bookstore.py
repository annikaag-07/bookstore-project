import mysql.connector
import pandas as pd
from config import DB_CONFIG


# Establish a global DB connection
db = mysql.connector.connect(**DB_CONFIG)
cursor = db.cursor()


def checkout():
    """Handle checkout process for the customer."""
    print("Welcome to checkout!! :D")
    st = int(input("Press 1 for store pickup, 2 for delivery: "))
    cid = input("Enter your customer ID: ")
    
    cursor.execute(f"SELECT * FROM `{cid}`")
    rs = cursor.fetchall()
    
    if not rs:
        print("Your cart is empty!")
        return
    
    print("Your cart items:")
    for row in rs:
        print(row)
    
    ck = int(input("Proceed to checkout? 1 for yes, 2 for no: "))
    if ck != 1:
        main_menu()
        return
    
    if st == 1:
        print("You can pick it up Monday-Friday, 7am-8pm. Pay at store :)")
    else:
        address = input("Enter your delivery address: ")
        codo = int(input("Press 1 for COD, 2 for online payment: "))
        if codo == 2:
            print("Thank you for shopping with us!")
            gp = int(input("1: Google Pay | 2: Apple Pay | 3: PhonePe: "))
            if gp in [1, 2, 3]:
                print("Please pay at +91 7723838286")


def customersupport():
    """Provide customer support options."""
    print("1. Order Assistance\n2. Product Enquiries\n3. Technical Support\n4. Email Support\n5. Phone Support")
    choice = int(input("Choose an option: "))
    
    if choice == 1:
        print("Order Assistance Options:\n1. Placing orders\n2. Tracking shipments\n3. Handling returns")
        oa = int(input("Choose option (0 for other): "))
        if oa == 1:
            print("Search for a book and add it to your cart.")
            main_menu()
        elif oa == 2:
            print("Track shipments at www.yellowdartshipment.com")
        elif oa == 3:
            returnbook()
        elif oa == 0:
            customersupport()
    elif choice == 2:
        seeall()
    elif choice == 3:
        issue = input("Describe the issue: ")
        email = input("Enter your email: ")
        print("We will work on fixing it and notify you via email.")
    elif choice == 4:
        print("Email us at Bookstorecustomersupport@gmail.com")
    elif choice == 5:
        print("Call us: +91 6757957585 or landline +91 0755 456534")


def returnbook():
    """Handle book return process."""
    bname = input("Enter book name to return: ")
    cursor.execute("SELECT * FROM books WHERE name=%s", (bname,))
    rs = cursor.fetchall()
    
    if rs:
        reason = input("Reason for return: ")
        print("Return Policy:\n1 week: Refund at store\n1 month: No refund\nAfter 1 month: Cannot return")
    else:
        print("Book not sold here.")
    
    cont = int(input("1 to continue browsing, 2 to exit: "))
    if cont == 1:
        main_menu()


def seeall():
    """Display all books and optionally add to cart."""
    cursor.execute("SELECT * FROM books")
    rs = cursor.fetchall()
    df = pd.DataFrame(rs, columns=["Name", "Author", "Price"])
    print(df)
    
    while True:
        i = int(input("Add a book to cart? 1: yes, 2: no: "))
        if i != 1:
            break
        b2 = input("Enter book name: ")
        qty = int(input("Quantity: "))
        cid = input("Customer ID: ")
        
        cursor.execute("SELECT price FROM books WHERE name=%s", (b2,))
        pr = cursor.fetchone()[0]
        total = pr * qty
        
        cursor.execute(f"INSERT INTO `{cid}` (book, price, qty) VALUES (%s, %s, %s)", (b2, total, qty))
        db.commit()
        print(f"{b2} added to cart.")
    
    main_menu()


def search():
    """Search for a book and optionally add to cart."""
    b1 = input("Enter book name: ")
    cursor.execute("SELECT * FROM books WHERE name=%s", (b1,))
    rs = cursor.fetchall()
    
    if rs:
        buy = int(input("Add this book to cart? 1: yes, 2: no: "))
        if buy == 1:
            cid = input("Customer ID: ")
            qty = int(input("Quantity: "))
            pr = rs[0][2]  # Assuming price is 3rd column
            total = pr * qty
            cursor.execute(f"INSERT INTO `{cid}` (book, price, qty) VALUES (%s, %s, %s)", (b1, total, qty))
            db.commit()
            print(f"{b1} added to cart.")
            check = int(input("Checkout? 1: yes, 2: no: "))
            if check == 1:
                checkout()
            else:
                search()
    else:
        print("Book not found.")


def books():
    """Search or view all books."""
    n2 = int(input("1: Search book, 2: See all books: "))
    if n2 == 1:
        search()
    else:
        seeall()


def signup():
    """Create new customer account."""
    cid = input("Enter customer ID: ")
    cursor.execute("SELECT * FROM login WHERE cid=%s", (cid,))
    if cursor.fetchone():
        print("ID taken, try again.")
        signup()
        return
    
    pwd = input("Enter password: ")
    cursor.execute("INSERT INTO login (cid, pwd) VALUES (%s, %s)", (cid, pwd))
    db.commit()
    cursor.execute(f"CREATE TABLE `{cid}` (book VARCHAR(1000), price INT, qty INT)")
    db.commit()
    print("Account created.")
    main_menu()


def login():
    """Login existing customer."""
    cid = input("Enter customer ID: ")
    pwd = input("Enter password: ")
    cursor.execute("SELECT * FROM login WHERE cid=%s AND pwd=%s", (cid, pwd))
    if cursor.fetchone():
        main_menu()
    else:
        print("Invalid credentials.")
        login()


def main_menu():
    """Main menu of bookstore."""
    print("1. Search book\n2. View cart\n3. Customer support\n4. Return book\n5. Checkout")
    chmain = int(input("Choose option: "))
    
    if chmain == 1:
        books()
    elif chmain == 2:
        cid = input("Customer ID: ")
        cursor.execute(f"SELECT * FROM `{cid}`")
        print(cursor.fetchall())
        main_menu()
    elif chmain == 3:
        customersupport()
    elif chmain == 4:
        returnbook()
    elif chmain == 5:
        checkout()


if __name__ == "__main__":
    print("1: Login | 2: Sign up")
    n = int(input("Choose option: "))
    if n == 1:
        login()
    else:
        signup()
