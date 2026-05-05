# src/repositories/user_repository.py
# (Аналогічна in-memory реалізація для користувачів)
from typing import Optional
from src.models.user import User
from src.repositories.base import IUserRepository

class InMemoryUserRepository(IUserRepository):
    def __init__(self):
        self._storage = {}
        self._current_id = 1

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self._storage.get(user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        for user in self._storage.values():
            if user.email == email:
                return user
        return None

    def save(self, user: User) -> User:
        if user.user_id == 0:
            user.user_id = self._current_id
            self._current_id += 1
        self._storage[user.user_id] = user
        return user