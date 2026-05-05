from typing import List
from src.repositories.base import IBookRepository, IUserRepository
from src.models.user import User
from src.models.book import Book
from src.dto.library_dto import BookResponseDTO

class LibraryService:
    def __init__(self, book_repo: IBookRepository, user_repo: IUserRepository):
        self.book_repo = book_repo
        self.user_repo = user_repo

    def register_user(self, name: str, email: str) -> User:
        if self.user_repo.get_by_email(email):
            raise ValueError(f"Користувач з email {email} вже існує.")

        new_user = User(user_id=0, name=name, email=email)
        return self.user_repo.save(new_user)

    def find_book_by_title(self, title: str) -> List[Book]:
        return self.book_repo.find_by_title(title)

    def borrow_book(self, user_id: int, book_id: int) -> Book:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError(f"Користувача з ID {user_id} не знайдено.")

        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise ValueError(f"Книгу з ID {book_id} не знайдено.")

        if book.is_borrowed:
            raise ValueError(f"Книга '{book.title}' вже позичена.")

        book.is_borrowed = True
        book.borrowed_by_id = user_id
        return self.book_repo.save(book)

    def return_book(self, book_id: int) -> Book:
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise ValueError(f"Книгу з ID {book_id} не знайдено.")

        if not book.is_borrowed:
            raise ValueError(f"Книга '{book.title}' зараз не позичена.")

        book.is_borrowed = False
        book.borrowed_by_id = None
        return self.book_repo.save(book)

    def find_book(self, query: str) -> list[BookResponseDTO]:
        all_books = self.book_repo.find_by_title("")  # Отримуємо всі книги для фільтрації
        found_books = []

        for book in all_books:
            if query.lower() in book.title.lower() or query.lower() in book.author.lower():
                status = "Позичена" if book.is_borrowed else "Доступна"
                # Конвертуємо Model у DTO
                dto = BookResponseDTO(book.book_id, book.title, book.author, status)
                found_books.append(dto)

        return found_books