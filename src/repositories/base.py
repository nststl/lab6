# src/repositories/base.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.book import Book
from src.models.user import User


class IBookRepository(ABC):
    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Book]: pass

    @abstractmethod
    def find_by_title(self, title: str) -> List[Book]: pass

    @abstractmethod
    def save(self, book: Book) -> Book: pass


class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]: pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]: pass

    @abstractmethod
    def save(self, user: User) -> User: pass