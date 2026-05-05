# src/repositories/book_repository.py
from typing import List, Optional
from src.models.book import Book
from src.repositories.base import IBookRepository

class InMemoryBookRepository(IBookRepository):
    def __init__(self):
        self._storage = {}
        self._current_id = 1

    def get_by_id(self, book_id: int) -> Optional[Book]:
        return self._storage.get(book_id)

    def find_by_title(self, title: str) -> List[Book]:
        return [book for book in self._storage.values()
                if title.lower() in book.title.lower()]

    def save(self, book: Book) -> Book:
        if book.book_id == 0:  # New book
            book.book_id = self._current_id
            self._current_id += 1
        self._storage[book.book_id] = book
        return book