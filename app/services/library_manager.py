import json
from pathlib import Path
from datetime import datetime

from app.models.book import Book
from app.models.member import Member


class LibraryManager:
    def __init__(self, db_path: str = "data/library_db.json"):
        self.books = {}  # Dictionary {book_id: Book_Object}
        self.members = {}  # Dictionary {member_id: Member_Object}
        self._book_id_counter = 101
        self._member_id_counter = 501
        self.db_path = Path(db_path)
        self._initialize_db_file()
        self.load_db()

    def _initialize_db_file(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.db_path.exists():
            self.save_db()

    def _backup_corrupt_db(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.db_path.with_name(f"{self.db_path.stem}.corrupt_{timestamp}{self.db_path.suffix}")
        try:
            self.db_path.replace(backup_path)
        except OSError:
            return None
        return backup_path

    def add_book(self, title: str, author: str):
        new_id = self._book_id_counter
        self.books[new_id] = Book(new_id, title, author)
        self._book_id_counter += 1
        self.save_db()
        return new_id

    def remove_book(self, book_id: int):
        book = self.books.get(book_id)
        if not book:
            return "Error: Book not found."
        if book.is_borrowed:
            return "Error: Cannot remove a borrowed book."

        del self.books[book_id]
        self.save_db()
        return f"Success: Book '{book.title}' removed."

    def register_member(self, name: str, password: str):
        new_id = self._member_id_counter
        member = Member(new_id, name)
        member.set_password(password)
        self.members[new_id] = member
        self._member_id_counter += 1
        self.save_db()
        return new_id

    def authenticate_member(self, member_id: int, password: str):
        member = self.members.get(member_id)
        if not member:
            return None
        if member.verify_password(password):
            return member
        return None

    def get_available_books(self):
        return [book for book in self.books.values() if not book.is_borrowed]

    def get_member_details(self, member_id: int):
        return self.members.get(member_id)

    def get_member_borrowed_books(self, member_id: int):
        member = self.members.get(member_id)
        if not member:
            return None
        return member.borrowed_books

    def get_member_return_history(self, member_id: int):
        member = self.members.get(member_id)
        if not member:
            return None
        return member.return_history

    def borrow_book(self, member_id: int, book_id: int):
        member = self.members.get(member_id)
        book = self.books.get(book_id)

        if not member or not book:
            return "Error: Member or Book not found."

        if book.is_borrowed:
            return "Error: Book is already borrowed."

        if not member.can_borrow():
            return "Error: Member has reached the limit of 3 books."


        book.is_borrowed = True
        member.borrowed_books.append(book)
        member.borrow_history.append(book.title)
        self.save_db()
        return f"Success: {member.name} borrowed '{book.title}'"

    def return_book(self, member_id: int, book_id: int):
        member = self.members.get(member_id)
        if not member:
            return "Error: Member not found."


        matching_books = [book for book in member.borrowed_books if book.id == book_id]
        if matching_books:
            for book in matching_books:
                book.is_borrowed = False
            member.borrowed_books = [book for book in member.borrowed_books if book.id != book_id]
            member.return_history.append(matching_books[0].title)
            self.save_db()
            return f"Success: '{matching_books[0].title}' returned."

        return "Error: This member does not have this book."

    def save_db(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "book_id_counter": self._book_id_counter,
            "member_id_counter": self._member_id_counter,
            "books": [
                {
                    "id": book.id,
                    "title": book.title,
                    "author": book.author,
                    "is_borrowed": book.is_borrowed,
                }
                for book in self.books.values()
            ],
            "members": [
                {
                    "id": member.id,
                    "name": member.name,
                    "password_salt": member.password_salt,
                    "password_hash": member.password_hash,
                    "borrowed_book_ids": [book.id for book in member.borrowed_books],
                    "borrow_history": member.borrow_history,
                    "return_history": member.return_history,
                }
                for member in self.members.values()
            ],
        }
        self.db_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def load_db(self):
        if not self.db_path.exists():
            return

        try:
            payload = json.loads(self.db_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            backup_path = self._backup_corrupt_db()
            self.save_db()
            if backup_path:
                print(f"Warning: Corrupt DB detected. Backup created at: {backup_path}")
            else:
                print("Warning: Corrupt DB detected. Started with a new empty DB.")
            return

        self._book_id_counter = payload.get("book_id_counter", 101)
        self._member_id_counter = payload.get("member_id_counter", 501)

        self.books = {}
        for book_data in payload.get("books", []):
            book = Book(book_data["id"], book_data["title"], book_data["author"])
            book.is_borrowed = book_data.get("is_borrowed", False)
            self.books[book.id] = book

        self.members = {}
        for member_data in payload.get("members", []):
            member = Member(
                member_data["id"],
                member_data["name"],
                member_data.get("password_salt", ""),
                member_data.get("password_hash", ""),
            )
            member.borrow_history = member_data.get("borrow_history", member_data.get("history", []))
            member.return_history = member_data.get("return_history", [])
            member.borrowed_books = [
                self.books[book_id]
                for book_id in member_data.get("borrowed_book_ids", [])
                if book_id in self.books
            ]
            self.members[member.id] = member
