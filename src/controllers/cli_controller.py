from src.services.library_service import LibraryService

class LibraryCLIController:
    def __init__(self, library_service: LibraryService):
        self.service = library_service

    def register_user_cmd(self, name: str, email: str):
        try:
            user = self.service.register_user(name, email)
            print(f"[УСПІХ] Користувача {user.name} зареєстровано з ID: {user.user_id}")
        except ValueError as e:
            print(f"[ПОМИЛКА] {e}")

    def find_book_cmd(self, title: str):
        books = self.service.find_book_by_title(title)
        if not books:
            print(f"[ІНФО] Книг за запитом '{title}' не знайдено.")
        for b in books:
            status = "Позичена" if b.is_borrowed else "Доступна"
            print(f"ID: {b.book_id} | {b.title} ({b.author}) - {status}")

    def borrow_book_cmd(self, user_id: int, book_id: int):
        try:
            book = self.service.borrow_book(user_id, book_id)
            print(f"[УСПІХ] Книгу '{book.title}' видано користувачу з ID {user_id}")
        except ValueError as e:
            print(f"[ПОМИЛКА] {e}")

    def return_book_cmd(self, book_id: int):
        try:
            book = self.service.return_book(book_id)
            print(f"[УСПІХ] Книгу '{book.title}' успішно повернуто в бібліотеку")
        except ValueError as e:
            print(f"[ПОМИЛКА] {e}")