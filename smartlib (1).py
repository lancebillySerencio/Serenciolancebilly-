import sys

books = [
    {"isbn": "1", "title": "Introduction to Computing", "author": "CITE Faculty", "category": "IT", "status": "Available"},
    {"isbn": "2", "title": "Database Management Systems", "author": "Aruleba & Oloyede", "category": "IT", "status": "Available"},
    {"isbn": "3", "title": "Web Application Architecture", "author": "Guo et al.", "category": "Web", "status": "Borrowed"}
]

users = {
    "student": {"password": "123", "role": "student"},
    "librarian": {"password": "admin", "role": "librarian"}
}

current_user = None

def clear_screen():
    print("\n" + "=" * 50 + "\n")

def login():
    global current_user
    clear_screen()
    print("--- SMARTLIB LOGIN SYSTEM ---")
    username = input("Enter Username (student/librarian): ").strip().lower()
    password = input("Enter Password: ").strip()

    if username in users and users[username]["password"] == password:
        current_user = {"username": username, "role": users[username]["role"]}
        print("\nLogin Successful! Welcome, " + username.capitalize() + " (" + current_user['role'].capitalize() + ").")
        input("\nPress Enter to continue...")
        return True
    else:
        print("\nInvalid Username or Password. Access Denied.")
        input("\nPress Enter to try again...")
        return False

def search_catalog():
    clear_screen()
    print("--- CATALOG SEARCH ---")
    query = input("Search by Title, Author, Category, or ISBN: ").strip().lower()
    
    results = [
        b for b in books 
        if query in b["title"].lower() or query in b["author"].lower() 
        or query in b["category"].lower() or query == b["isbn"]
    ]

    print("\nFound " + str(len(results)) + " matching book(s):\n")
    print(f"{'ISBN':<8} | {'Title':<30} | {'Author':<20} | {'Status':<10}")
    print("-" * 75)
    for b in results:
        print(f"{b['isbn']:<8} | {b['title']:<30} | {b['author']:<20} | {b['status']:<10}")

def add_book():
    clear_screen()
    print("--- ADD NEW BOOK ---")
    isbn = input("Enter Book ISBN (e.g., 4): ").strip()
    
    # Check if ISBN already exists
    for book in books:
        if book["isbn"] == isbn:
            print("Error: A book with this ISBN already exists!")
            return
            
    title = input("Enter Book Title: ").strip()
    author = input("Enter Author: ").strip()
    category = input("Enter Category (e.g., IT, Web, Fiction): ").strip()
    
    if not isbn or not title or not author or not category:
        print("Error: All fields are required!")
        return
        
    books.append({
        "isbn": isbn,
        "title": title,
        "author": author,
        "category": category,
        "status": "Available"
    })
    print(f"\nSuccess: Book '{title}' has been added successfully!")

def edit_book():
    clear_screen()
    print("--- EDIT BOOK DETAILS ---")
    isbn = input("Enter ISBN of the book to edit: ").strip()
    
    for book in books:
        if book["isbn"] == isbn:
            print(f"\nCurrent Details -> Title: {book['title']} | Author: {book['author']} | Category: {book['category']}")
            
            new_title = input("Enter new Title (press Enter to keep current): ").strip()
            if new_title:
                book['title'] = new_title
                
            new_author = input("Enter new Author (press Enter to keep current): ").strip()
            if new_author:
                book['author'] = new_author
                
            new_category = input("Enter new Category (press Enter to keep current): ").strip()
            if new_category:
                book['category'] = new_category
                
            print("\nSuccess: Book details updated successfully!")
            return
    print("\nError: Book with provided ISBN not found.")

def delete_book():
    clear_screen()
    print("--- DELETE BOOK ---")
    isbn = input("Enter ISBN of the book to delete: ").strip()
    
    for i, book in enumerate(books):
        if book["isbn"] == isbn:
            confirm = input(f"Are you sure you want to delete '{book['title']}'? (y/n): ").strip().lower()
            if confirm == 'y':
                removed = books.pop(i)
                print(f"\nSuccess: Book '{removed['title']}' has been removed from the catalog.")
            else:
                print("\nDeletion cancelled.")
            return
    print("\nError: Book with provided ISBN not found.")

def process_transaction(action):
    clear_screen()
    print("--- PROCESS " + action.upper() + " TRANSACTION ---")
    isbn = input("Enter Book ISBN: ").strip()
    
    for book in books:
        if book["isbn"] == isbn:
            if action == "borrow":
                if book["status"] == "Available":
                    book["status"] = "Borrowed"
                    print("\nSuccess: '" + book['title'] + "' has been marked as BORROWED.")
                else:
                    print("\nError: Book is currently borrowed or unavailable.")
            elif action == "return":
                if book["status"] == "Borrowed":
                    book["status"] = "Available"
                    print("\nSuccess: '" + book['title'] + "' has been returned and marked AVAILABLE.")
                else:
                    print("\nError: Book is already marked as available.")
            return
    print("\nError: Book with provided ISBN not found.")

def generate_inventory_report():
    clear_screen()
    print("--- REAL-TIME INVENTORY REPORT ---")
    total = len(books)
    available = sum(1 for b in books if b["status"] == "Available")
    borrowed = sum(1 for b in books if b["status"] == "Borrowed")

    print("Total Books: " + str(total) + " | Available: " + str(available) + " | Borrowed: " + str(borrowed) + "\n")
    print(f"{'ISBN':<8} | {'Title':<30} | {'Category':<12} | {'Status':<10}")
    print("-" * 65)
    for b in books:
        print(f"{b['isbn']:<8} | {b['title']:<30} | {b['category']:<12} | {b['status']:<10}")

def student_menu():
    while True:
        clear_screen()
        print("=== SMARTLIB STUDENT PORTAL ===")
        print("1. Search Book Catalog")
        print("2. View All Available Books")
        print("3. Logout")
        
        choice = input("Select an option (1-3): ").strip()
        if choice == "1":
            search_catalog()
        elif choice == "2":
            clear_screen()
            print("--- AVAILABLE BOOKS ---")
            for b in books:
                if b["status"] == "Available":
                    print("[" + b['isbn'] + "] " + b['title'] + " by " + b['author'] + " (" + b['category'] + ")")
        elif choice == "3":
            print("Logging out...")
            break
        else:
            print("Invalid choice! Try again.")
        input("\nPress Enter to continue...")

def librarian_menu():
    while True:
        clear_screen()
        print("=== SMARTLIB LIBRARIAN ADMIN PANEL ===")
        print("1. Search Book Catalog")
        print("2. Add New Book")
        print("3. Edit Book Details")
        print("4. Delete Book")
        print("5. Process Borrow Transaction")
        print("6. Process Return Transaction")
        print("7. View Real-Time Inventory Report")
        print("8. Logout")

        choice = input("Select an option (1-8): ").strip()
        if choice == "1":
            search_catalog()
        elif choice == "2":
            add_book()
        elif choice == "3":
            edit_book()
        elif choice == "4":
            delete_book()
        elif choice == "5":
            process_transaction("borrow")
        elif choice == "6":
            process_transaction("return")
        elif choice == "7":
            generate_inventory_report()
        elif choice == "8":
            print("Logging out...")
            break
        else:
            print("Invalid choice! Try again.")
        input("\nPress Enter to continue...")

def main():
    while True:
        clear_screen()
        print(" SmartLib: Console-Based Library Information System")