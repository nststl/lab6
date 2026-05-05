# src/models/book.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class Book:
    book_id: int
    title: str
    author: str
    is_borrowed: bool = False
    borrowed_by_id: Optional[int] = None