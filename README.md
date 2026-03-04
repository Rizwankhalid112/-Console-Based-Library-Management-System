# Console-Based Library Management System

A modular Library Management System built with Python and a JSON file as storage.

## Features

- Member register/login with auto-generated member IDs
- Passwords stored as salted hashes (PBKDF2-HMAC-SHA256)
- Add and remove books with auto-generated book IDs
- Borrow and return books with rule checks
- View available books
- View member details, borrowed books, and return history
- Back navigation (`b`) in input flows
- Automatic `data/` + `library_db.json` creation on first run
- Corrupt JSON backup and safe recovery

## Rules Enforced

- A book cannot be borrowed if already borrowed
- A member cannot borrow more than 3 books at a time
- Returning a book updates availability immediately
- Borrow and return history are persisted

## Project Structure

```text
Library_Management_System/
├── app/
│   ├── models/
│   │   ├── book.py
│   │   └── member.py
│   ├── services/
│   │   └── library_manager.py
│   └── utils/
│       └── helpers.py
├── main.py
├── data/
│   └── library_db.json
└── README.md
```

## Run

```bash
python3 main.py
```
