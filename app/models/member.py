import hashlib
import secrets


class Member:
    def __init__(
        self,
        member_id: int,
        name: str,
        password_salt: str = "",
        password_hash: str = "",
    ):
        self.id = member_id
        self.name = name
        self.password_salt = password_salt
        self.password_hash = password_hash
        self.borrowed_books = []  # List to store Book objects
        self.borrow_history = []  # List to store titles of books ever borrowed
        self.return_history = []  # List to store titles of books returned

    def can_borrow(self) -> bool:
        return len(self.borrowed_books) < 3

    @staticmethod
    def _hash_password(password: str, salt_hex: str) -> str:
        salt = bytes.fromhex(salt_hex)
        hashed = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
        return hashed.hex()

    def set_password(self, password: str):
        self.password_salt = secrets.token_hex(16)
        self.password_hash = self._hash_password(password, self.password_salt)

    def verify_password(self, password: str) -> bool:
        if not self.password_salt or not self.password_hash:
            return False
        return self._hash_password(password, self.password_salt) == self.password_hash

    def __str__(self):
        return f"[Member ID: {self.id}] Name: {self.name} | Books Held: {len(self.borrowed_books)}"
