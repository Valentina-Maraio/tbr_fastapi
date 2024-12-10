# app/crud.py
from typing import List, Optional
from app.models import Book

# In-memory storage for books
books: List[Book] = []

def get_books(title: Optional[str] = None, author: Optional[str] = None, read: Optional[bool] = None) -> List[Book]:
    """
    Retrieve books with optional filters for title, author, and read status
    """
    filtered_books = books
    if title:
        filtered_books = [book for book in filtered_books if title.lower() in book.title.lower()]
    if author:
        filtered_books = [book for book in filtered_books if author.lower() in book.author.lower()]
    if read is not None:
        filtered_books = [book for book in filtered_books if book.read == read]
    return filtered_books

def get_book(book_id: int) -> Optional[Book]:
    """Retrieve a book by its ID"""
    return next((book for book in books if book.id == book_id), None)

def create_book(book: Book) -> Book:
    """Create a new book"""
    if any(b.id == book.id for b in books):
        return None
    books.append(book)
    return book

def update_book(book_id: int, updated_book: Book) -> Optional[Book]:
    """Update a book"""
    book_index = next((index for index, book in enumerate(books) if book.id == book_id), None)
    if book_index is None:
        return None
    books[book_index] = updated_book
    return updated_book

def delete_book(book_id: int) -> Optional[Book]:
    """Delete a book by its ID"""
    book_index = next((index for index, book in enumerate(books) if book.id == book_id), None)
    if book_index is None:
        return None
    deleted_book = books.pop(book_index)
    return deleted_book
