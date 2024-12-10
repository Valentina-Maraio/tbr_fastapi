from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Initialize the FastAPI app
app = FastAPI()

# Data model for a book
class Book(BaseModel):
	id: int
	title: str
	author: str
	comment: Optional[str] = None
	read: bool = False
	
# In-memory storage for books
books: List[Book] = []

@app.get("/")
def read_root():
	'''
	Root endpoint to confirm the API is running.
	'''
	return {"message": "Welcome to the Book Collection API!"}

@app.get('/books', response_model=List[Book])
def get_books():
	'''
	Retrieve all books in the collection
	'''
	return books

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
	'''
	Retrieve a specific book by ID.
	'''
	book = next((book for book in books if book.id == book_id), None)
	if not book:
		raise HTTPException(status_code=404, detail="Book not found")
	return book

@app.post("/books", response_model=Book)
def create_book(book: Book):
	'''
	Add a new book to the collection
	'''
	if any(b.id == book.id for b in books):
		raise HTTPException(status_code=400, detail="Book ID already exists")
	books.append(book)
	return book

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book):
	'''
	Update details of an existing book
	'''
	book_index = next((index for index, book in enumerate(books) if book.id == book_id), None)
	if book_index is None:
		raise HTTPException(status_code=404, detail="Book not found")
	books[book_index] = updated_book
	return updated_book

@app.delete("/books/{book_id}", response_model=Book)
def delete_book(book_id: int):
	'''
	Remove a book from the collection by ID
	'''
	book_index = next((index for index, book in enumerate(books) if book.id == book_id), None)
	if book_index is None:
		raise HTTPException(status_code=404, detail="Book not found")
	deleted_book = books.pop(book_index)
	return deleted_book
