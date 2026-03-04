# Console-Based Library Management System

A robust, modular, and Object-Oriented Library Management System built with Python. This project demonstrates clean code practices, separation of concerns, and efficient data management without the use of external libraries or databases.

## 🚀 Features

### **Book Management**
* **Add/Remove Books:** Dynamically manage the library inventory.
* **Availability Tracking:** Real-time updates on whether a book is available or borrowed.
* **Unique Identification:** Auto-generated unique IDs for every book.

### **Member Management**
* **Registration:** Register new members with unique system IDs.
* **Borrowing Limits:** Enforces a strict rule of maximum **3 books** per member.
* **Borrow History:** Tracks every book a member has interacted with.

### **System Rules**
* Prevents borrowing of already borrowed books.
* Automated ID generation for Books and Members.
* Comprehensive console-based interactive menu.

---

## 🏗️ Project Structure

The project follows a professional modular structure:

```text
Library_Management_System/
├── app/
│   ├── models/          # Data structures (Book, Member)
│   ├── services/        # Business logic (LibraryManager)
│   ├── utils/           # Helper functions
│   └── main.py          # Entry point & CLI Menu
├── .gitignore           # Git exclusion rules
├── requirements.txt     # Dependency list (Standard practice)
└── README.md            # Documentation
