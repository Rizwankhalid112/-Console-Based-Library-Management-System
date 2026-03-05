from pathlib import Path

from app.services.library_manager import LibraryManager
from app.utils.helpers import (
    prompt_int_or_back,
    prompt_member_name_or_back,
    prompt_non_empty_or_back,
    prompt_password_or_back,
)



def print_auth_menu() -> None:
    print("\n=== Member Access ===")
    print("1. Login")
    print("2. Register")
    print("0. Exit")


def print_menu() -> None:
    print("\n=== Library Management System ===")
    print("1. Add book")
    print("2. Remove book")
    print("3. View available books")
    print("4. View member details")
    print("5. Borrow book")
    print("6. Return book")
    print("7. View borrowed books for a member")
    print("8. View returned books history for a member")
    print("9. View specific member details (by ID)")
    print("10. View borrowed books for specific member (by ID)")
    print("0. Exit")




def authenticate_or_register(manager: LibraryManager):
    while True:
        print_auth_menu()
        choice = input("Select an option: ").strip()

        if choice == "1":
            member_id = prompt_int_or_back("Member ID")
            if member_id is None:
                continue
            password = prompt_password_or_back("Password")
            if password is None:
                continue
            member = manager.authenticate_member(member_id, password)
            if member:
                print(f"Login successful. Welcome, {member.name}.")
                return member
            print("Error: Invalid Member ID or password.")
        elif choice == "2":
            name = prompt_member_name_or_back("Name")
            if name is None:
                continue
            password = prompt_password_or_back("Set password")
            if password is None:
                continue
            member_id = manager.register_member(name, password)
            print(f"Registration successful. Your Member ID is: {member_id}")
            print("Please login using your Member ID and password.")
        elif choice == "0":
            return None
        else:
            print("Invalid option. Please choose from the menu.")


def list_available_books(manager: LibraryManager) -> None:
    available_books = manager.get_available_books()
    if not available_books:
        print("No available books.")
        return
    print("\nAvailable Books:")
    for book in available_books:
        print(f"- {book}")


def show_member_details(manager: LibraryManager, member_id: int) -> None:
    member = manager.get_member_details(member_id)
    if not member:
        print("Error: Member not found.")
        return
    print(f"\nMember: {member}")
    if member.borrowed_books:
        print("Currently borrowed books:")
        for book in member.borrowed_books:
            print(f"- ID: {book.id} | Title: {book.title}")
    else:
        print("Currently borrowed books: None")

    if member.borrow_history:
        print("Borrow history:")
        for title in member.borrow_history:
            print(f"- {title}")
    else:
        print("Borrow history: None")

    if member.return_history:
        print("Return history:")
        for title in member.return_history:
            print(f"- {title}")
    else:
        print("Return history: None")


def show_member_borrowed_books(manager: LibraryManager, member_id: int) -> None:
    borrowed_books = manager.get_member_borrowed_books(member_id)
    if borrowed_books is None:
        print("Error: Member not found.")
        return
    if not borrowed_books:
        print("This member currently has no borrowed books.")
        return
    print("\nBorrowed Books:")
    for book in borrowed_books:
        print(f"- {book}")


def show_member_return_history(manager: LibraryManager, member_id: int) -> None:
    return_history = manager.get_member_return_history(member_id)
    if return_history is None:
        print("Error: Member not found.")
        return
    if not return_history:
        print("No returned books in history for this member.")
        return
    print("\nReturned Books History:")
    for title in return_history:
        print(f"- {title}")


def show_specific_member_details(manager: LibraryManager) -> None:
    member_id = prompt_int_or_back("Member ID")
    if member_id is None:
        return
    show_member_details(manager, member_id)


def show_specific_member_borrowed_books(manager: LibraryManager) -> None:
    member_id = prompt_int_or_back("Member ID")
    if member_id is None:
        return
    show_member_borrowed_books(manager, member_id)


def run() -> None:
    db_path = Path(__file__).resolve().parent / "data" / "library_db.json"
    manager = LibraryManager(str(db_path))
    logged_in_member = authenticate_or_register(manager)
    if not logged_in_member:
        print("Exiting.")
        return
    current_member_id = logged_in_member.id

    while True:
        print_menu()
        choice = input("Select an option: ").strip()

        if choice == "1":
            title = prompt_non_empty_or_back("Book title")
            if title is None:
                continue
            author = prompt_non_empty_or_back("Author")
            if author is None:
                continue
            book_id = manager.add_book(title, author)
            print(f"Book added with ID: {book_id}")
        elif choice == "2":
            book_id = prompt_int_or_back("Book ID to remove")
            if book_id is None:
                continue
            print(manager.remove_book(book_id))
        elif choice == "3":
            list_available_books(manager)
        elif choice == "4":
            show_member_details(manager, current_member_id)
        elif choice == "5":
            book_id = prompt_int_or_back("Book ID")
            if book_id is None:
                continue
            print(manager.borrow_book(current_member_id, book_id))
        elif choice == "6":
            book_id = prompt_int_or_back("Book ID")
            if book_id is None:
                continue
            print(manager.return_book(current_member_id, book_id))
        elif choice == "7":
            show_member_borrowed_books(manager, current_member_id)
        elif choice == "8":
            show_member_return_history(manager, current_member_id)
        elif choice == "9":
            show_specific_member_details(manager)
        elif choice == "10":
            show_specific_member_borrowed_books(manager)
        elif choice == "0":
            print("Exiting.")
            break
        else:
            print("Invalid option. Please choose from the menu.")


if __name__ == "__main__":
    run()
