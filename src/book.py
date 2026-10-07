"""
Module: book.py
Description: Defines the Book class which models individual library books,
their attributes (title, author, ISBN), and their availability status.
ISBN(The unique International Standard Book Number.)
"""

class Book:
    """Represents a book with a title, author, unique ISBN, and availability state."""
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = True # By default, a new book is available for borrowing

    def borrow_book(self):
        """
        Marks the book as borrowed if it is currently available.        
        Returns:
            bool: True if the book was successfully borrowed, False if already borrowed.
        """
        if self.is_available:
            self.is_available = False
            return True
        return False

    def return_book(self):
        """Marks the book as returned, setting its availability back to True."""
        self.is_available = True

    def __str__(self):
        """
        Returns a human-readable string representation of the book object.
        """
        status = "Available" if self.is_available else "Borrowed"
        return f"'{self.title}' par {self.author} (ISBN: {self.isbn}) - Status : {status}"

