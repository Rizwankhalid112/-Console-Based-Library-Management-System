# Console-Based Library Management System

A robust, modular, and Object-Oriented Library Management System built with Python. This project demonstrates clean code practices, separation of concerns, and secure data persistence using JSON, without the need for external databases.

## 🚀 Features

### **Security & Persistence**
* **Secure Authentication:** Passwords are never stored in plain text; they use salted hashes (PBKDF2-HMAC-SHA256).
* **JSON Storage:** Automatic creation of `data/library_db.json` with built-in corruption recovery and backups.
* **Session Management:** Member login/register flow with persistent session IDs.

### **Book Management**
* **Inventory Control:** Add and remove books with auto-generated unique IDs.
* **Availability Tracking:** Real-time status updates (Available vs. Borrowed).
* **Search & View:** Easily list all available books in the library.

### **Member Management**
* **Borrowing Rules:** Enforces a strict limit of **3 books** per member.
* **History Tracking:** Comprehensive logs for both borrowed and returned books.
* **UX Navigation:** Integrated "Back" navigation (`b`) in all input prompts for a smooth CLI experience.

---

## 🏗️ Project Structure

The project follows a professional N-tier modular architecture:

```text
Library_Management_System/
├── app/
│   ├── models/          # Data structures & Security logic (Book, Member)
│   ├── services/        # Business logic & Persistence (LibraryManager)
│   ├── utils/           # Input validation & Regex helpers
│   └── main.py          # Entry point & CLI Controller
├── data/                # Local JSON database storage
├── .gitignore           # Git exclusion rules
├── requirements.txt     # Dependency list
└── README.md            # Documentation