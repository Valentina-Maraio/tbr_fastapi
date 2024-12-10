# app/models.py
from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    id: int
    title: str
    author: str
    comment: Optional[str] = None
    read: bool = False
