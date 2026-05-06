import os
import psycopg2
from src.repositories.book_repository import InMemoryBookRepository
from src.repositories.user_repository import InMemoryUserRepository
from src.services.library_service import LibraryService
from src.controllers.cli_controller import LibraryCLIController
from src.models.book import Book


def get_db_connection():
    print("\n=== Налаштування підключення до Бази Даних ===")
    print("Натисніть Enter, щоб використати значення за замовчуванням (з Docker)")

    host = input(f"Хост [{os.getenv('DB_HOST', 'localhost')}]: ") or os.getenv('DB_HOST', 'localhost')
    port = input(f"Порт [{os.getenv('DB_PORT', '5432')}]: ") or os.getenv('DB_PORT', '5432')
    user = input(f"Користувач [{os.getenv('DB_USER', 'admin')}]: ") or os.getenv('DB_USER', 'admin')
    password = input(f"Пароль [{os.getenv('DB_PASSWORD', 'secret')}]: ") or os.getenv('DB_PASSWORD', 'secret')
    dbname = input(f"Назва БД [{os.getenv('DB_NAME', 'library')}]: ") or os.getenv('DB_NAME', 'library')

    try:
        conn = psycopg2.connect(host=host, port=port, user=user, password=password, dbname=dbname)
        print("\n[УСПІХ] Успішно підключено до реальної БД PostgreSQL!")

        # Тут ми створюємо тестову таблицю, щоб довести, що БД працює
        with conn.cursor() as cur:
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS books_test
                        (
                            id
                            SERIAL
                            PRIMARY
                            KEY,
                            title
                            VARCHAR
                        (
                            100
                        )
                            )
                        """)
            conn.commit()
        return conn
    except Exception as e:
        print(f"\n[УВАГА] Не вдалося підключитися до реальної БД ({e}).")
        print("Продовжуємо роботу з тестовою пам'яттю (InMemory).")
        return None


def main():
    # 1. Спроба підключитися до реальної БД з консолі
    db_conn = get_db_connection()

    # 2. Ініціалізуємо репозиторії (якщо БД є - можна було б передати туди db_conn)
    book_repo = InMemoryBookRepository()
    user_repo = InMemoryUserRepository()

    # Додамо кілька книг для перевірки логіки
    book_repo.save(Book(book_id=0, title="Чистий код", author="Роберт Мартін"))

    # 3. Ініціалізуємо сервіс та контролер
    service = LibraryService(book_repo, user_repo)
    controller = LibraryCLIController(service)

    # 4. Демонстрація роботи
    print("\n--- Робота системи ---")
    controller.register_user_cmd("Олександр", "alex@example.com")
    controller.find_book_cmd("код")


if __name__ == "__main__":
    main()