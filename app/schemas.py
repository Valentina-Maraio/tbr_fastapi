# app/schemas.py
from typing import List, Optional
from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    comment: Optional[str] = None
    read: bool = False

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class Book(BookBase):
    id: int

class BookListResponse(BaseModel):
    books: List[Book]
