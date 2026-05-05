# main.py
from src.repositories.book_repository import InMemoryBookRepository
from src.repositories.user_repository import InMemoryUserRepository
from src.services.library_service import LibraryService
from src.controllers.cli_controller import LibraryCLIController
from src.models.book import Book


def main():
    # 1. Ініціалізуємо репозиторії
    book_repo = InMemoryBookRepository()
    user_repo = InMemoryUserRepository()

    # Додамо кілька книг для перевірки
    book_repo.save(Book(book_id=0, title="Чистий код", author="Роберт Мартін"))
    book_repo.save(Book(book_id=0, title="Патерни проектування", author="Банда чотирьох"))

    # 2. Ініціалізуємо сервіс
    service = LibraryService(book_repo, user_repo)

    # 3. Ініціалізуємо контролер
    controller = LibraryCLIController(service)

    # 4. Викликаємо команди через контролер
    print("--- Реєстрація ---")
    controller.register_user_cmd("Олександр", "alex@example.com")

    print("\n--- Пошук ---")
    controller.find_book_cmd("код")

    print("\n--- Видача книги ---")
    controller.borrow_book_cmd(user_id=1, book_id=1)

    print("\n--- Повторний пошук (щоб побачити статус) ---")
    controller.find_book_cmd("код")


if __name__ == "__main__":
    main()