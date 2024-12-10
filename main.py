from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.future import select

# Initialize FastAPI
app = FastAPI()

# SQLAlchemy setup
DATABASE_URL = "sqlite:///./books.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database model
class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    comment = Column(String, nullable=True)
    read = Column(Boolean, default=False)

# Pydantic model for validation
class BookCreate(BaseModel):
    title: str
    author: str
    comment: Optional[str] = None
    read: bool = False

class Book(BaseModel):
    id: int
    title: str
    author: str
    comment: Optional[str]
    read: bool

    class Config:
        orm_mode = True

# Create database tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Book Collection API!"}

# Get all books
@app.get("/books", response_model=List[Book])
def get_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = db.execute(select(BookModel).offset(skip).limit(limit)).scalars().all()
    return books

# Add a new book
@app.post("/books", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = BookModel(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

# Get a specific book by ID
@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(BookModel, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# Update a book
@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: BookCreate, db: Session = Depends(get_db)):
    book = db.get(BookModel, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in updated_book.dict().items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book

# Delete a book
@app.delete("/books/{book_id}", response_model=Book)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(BookModel, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return book
