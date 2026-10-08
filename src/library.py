"""
Module: library.py
Description: Manages the collection of books, persistence in JSON format,
and library operations (add, update, delete, borrow, return).
"""

import json
import os
from src.book import Book


class Library:
    """Handles the catalog of books and persistence operations using books.json."""

    def __init__(self, data_file="data/books.json"):
        """Initializes the Library instance and loads books from storage."""

        self.data_file = data_file
        self.books = []
        self.load_books()

    def load_books(self):
        """Loads books from the JSON file and reconstructs Book objects with their states."""

        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    self.books = [Book(item["title"], item["author"], item["isbn"]) for item in data]
                    for i, item in enumerate(data):
                        self.books[i].is_available = item.get("is_available", True)
            except json.JSONDecodeError:
                self.books = []
        else:
            self.books = []

    def save_books(self):
        """Saves the current list of books and their states to the JSON file."""

        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        data = [{
            "title": b.title,
            "author": b.author,
            "isbn": b.isbn,
            "is_available": b.is_available
        } for b in self.books]

        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def add_book(self, title, author, isbn):
        """Adds a new book to the library catalog (Admin privilege)."""

        for b in self.books:
            if b.isbn == isbn:
                print("X Error : A book with this ISBN already exists.")
                return
        new_book = Book(title, author, isbn)
        self.books.append(new_book)
        self.save_books()
        print("Book added successfully !")

    def update_book(self, isbn, new_title, new_author):
        """Updates an existing book's title and author by its ISBN (Admin privilege)."""

        for book in self.books:
            if book.isbn == isbn:
                book.title = new_title
                book.author = new_author
                self.save_books()
                print("Book updated successfully !")
                return
        print("X Error : Book not found")

    def delete_book(self, isbn):
        """Removes a book from the library catalog by its ISBN (Admin privilege)."""

        for book in self.books:
            if book.isbn == isbn:
                self.books.remove(book)
                self.save_books()
                print("Book deleted successfully !")
                return
        print("X Error : book not found.")

    def list_books(self):
        """Displays all books currently registered in the library catalog."""

        if not self.books:
            print(" Any book found in the library.")
            return
        print("\n--- LIST OF BOOKS ---")
        for i, book in enumerate(self.books, 1):
            print(f"{i}. {book}")
  
    def borrow_book(self, isbn):
        """Allows borrowing a book by specifying its ISBN."""

        for book in self.books:
            if book.isbn == isbn:
                if book.borrow_book():
                    self.save_books()
                    print(f"You borrowed : '{book.title}'")
                else:
                    print(" This book is already borrowed.")
                return
        print(" Book not found.")

    def return_book(self, isbn):
        """Allows returning a borrowed book by specifying its ISBN."""
        
        for book in self.books:
            if book.isbn == isbn:
                book.return_book()
                self.save_books()
                print(f"Book returned successfully : '{book.title}'")
                return
        print("X Error : Book not found.")

    