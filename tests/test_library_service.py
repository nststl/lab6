import pytest
from src.models.book import Book
from src.repositories.book_repository import InMemoryBookRepository
from src.repositories.user_repository import InMemoryUserRepository
from src.services.library_service import LibraryService


@pytest.fixture
def library_service():
    """Фікстура для налаштування чистого середовища перед кожним тестом"""
    book_repo = InMemoryBookRepository()
    user_repo = InMemoryUserRepository()

    # Додаємо тестові дані
    book_repo.save(Book(book_id=0, title="Чистий код", author="Роберт Мартін"))
    book_repo.save(Book(book_id=0, title="Патерни проектування", author="Банда чотирьох"))

    return LibraryService(book_repo, user_repo)


# 1. Реєстрація нового користувача (Позитивний)
def test_register_new_user_success(library_service):
    user = library_service.register_user("Олександр", "alex@test.com")
    assert user.user_id == 1
    assert user.name == "Олександр"


# 2. Спроба зареєструвати існуючий email (Негативний)
def test_register_user_duplicate_email(library_service):
    library_service.register_user("Олександр", "alex@test.com")
    with pytest.raises(ValueError, match="вже існує"):
        library_service.register_user("Іван", "alex@test.com")


# 3. Пошук книги 
def test_find_book_by_title_or_author(library_service):
    # Пошук за назвою
    books_by_title = library_service.find_book("чистий")
    assert len(books_by_title) == 1
    assert books_by_title[0].title == "Чистий код"

    # Пошук за автором
    books_by_author = library_service.find_book("банда")
    assert len(books_by_author) == 1
    assert books_by_author[0].author == "Банда чотирьох"

    # Перевірка формату DTO
    assert hasattr(books_by_author[0], 'status')


# 4. Успішне позичання книги відповідному читачу (Позитивний)
def test_borrow_book_success(library_service):
    user = library_service.register_user("Олександр", "alex@test.com")
    book = library_service.borrow_book(user.user_id, 1)  # Беремо "Чистий код"
    assert book.is_borrowed is True
    assert book.borrowed_by_id == user.user_id


# 5. Спроба позичити книгу користувачу, якого не існує (Негативний)
def test_borrow_book_invalid_user(library_service):
    with pytest.raises(ValueError, match="не знайдено"):
        library_service.borrow_book(999, 1)


# 6. Спроба позичити книгу, яка вже позичена (Негативний)
def test_borrow_already_borrowed_book(library_service):
    user1 = library_service.register_user("Олександр", "alex@test.com")
    user2 = library_service.register_user("Іван", "ivan@test.com")

    library_service.borrow_book(user1.user_id, 1)

    with pytest.raises(ValueError, match="вже позичена"):
        library_service.borrow_book(user2.user_id, 1)


# 7. Повернення книги (Позитивний)
def test_return_book_success(library_service):
    user = library_service.register_user("Олександр", "alex@test.com")
    library_service.borrow_book(user.user_id, 1)

    book = library_service.return_book(1)
    assert book.is_borrowed is False
    assert book.borrowed_by_id is None


# 8. Спроба повернути книгу, яка не позичена (Негативний)
def test_return_not_borrowed_book(library_service):
    with pytest.raises(ValueError, match="зараз не позичена"):
        library_service.return_book(1)