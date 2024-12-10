# app/main.py
from fastapi import FastAPI, HTTPException
from typing import List, Optional
from app.models import Book
from app.schemas import BookCreate, BookUpdate, BookListResponse
from app.crud import get_books, get_book, create_book, update_book, delete_book

app = FastAPI()

@app.get("/", response_model=dict)
def read_root():
    return {"message": "Welcome to the Book Collection API!"}

@app.get("/books", response_model=BookListResponse)
def list_books(title: Optional[str] = None, author: Optional[str] = None, read: Optional[bool] = None):
    """
    Retrieve all books in the collection with optional search filters for title, author, and read status
    """
    books = get_books(title=title, author=author, read=read)
    return BookListResponse(books=books)

@app.get("/books/{book_id}", response_model=Book)
def get_book_details(book_id: int):
    """
    Retrieve a specific book by ID
    """
    book = get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books", response_model=Book)
def create_new_book(book: BookCreate):
    """
    Add a new book to the collection
    """
    created_book = create_book(book)
    if not created_book:
        raise HTTPException(status_code=400, detail="Book ID already exists")
    return created_book

@app.put("/books/{book_id}", response_model=Book)
def update_book_details(book_id: int, updated_book: BookUpdate):
    """
    Update details of an existing book
    """
    updated = update_book(book_id, updated_book)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated

@app.delete("/books/{book_id}", response_model=Book)
def remove_book(book_id: int):
    """
    Remove a book from the collection by ID
    """
    deleted_book = delete_book(book_id)
    if not deleted_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return deleted_book
