class Book:
    def __init__(self, book_id: int, title: str, author: str):
        self.id = book_id
        self.title = title
        self.author = author
        self.is_borrowed = False

    def __str__(self):
        status = "Borrowed" if self.is_borrowed else "Available"
        return f"[ID: {self.id}] {self.title} by {self.author} - ({status})"