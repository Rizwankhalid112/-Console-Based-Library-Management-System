import re


def prompt_non_empty(message: str) -> str:
    while True:
        value = input(message).strip()
        if value:
            return value
        print("Input cannot be empty.")


def prompt_int(message: str) -> int:
    while True:
        raw_value = input(message).strip()
        try:
            return int(raw_value)
        except ValueError:
            print("Please enter a valid integer.")


def prompt_password(message: str) -> str:
    while True:
        value = input(message).strip()
        if value:
            return value
        print("Password cannot be empty.")


def prompt_member_name(message: str) -> str:
    while True:
        value = input(message).strip()
        normalized = " ".join(value.split())
        if len(normalized) < 2:
            print("Please enter a valid name (at least 2 letters).")
            continue
        if not re.fullmatch(r"[A-Za-z][A-Za-z\s'-]*", normalized):
            print("Name can contain letters, spaces, apostrophes, and hyphens only.")
            continue
        if not any(char.isalpha() for char in normalized):
            print("Please enter a valid name.")
            continue
        return normalized
