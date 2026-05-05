# Лабораторна робота 5: Бізнес-логіка, сервіси, модульне тестування

## 1. Опис реалізованих бізнес-сценаріїв
У рамках системи управління бібліотекою реалізовано 4 ключові сценарії:
1. **Реєстрація користувача:** Система створює нового читача, запобігаючи дублюванню електронних адрес.
2. **Пошук книги:** Дозволяє знаходити книжки за частковим збігом назви.
3. **Кредитування книги (Видача):** Перевіряє валідність читача та статус книги. Змінює стан книги на "позичена" та прив'язує ID читача, запобігаючи подвійній видачі однієї книги.
4. **Повернення книги:** Знімає статус "позичена" та відкріплює ID користувача, роблячи книгу доступною для інших.

## 2. Структура коду (Controller-Service-Repository)
Проєкт дотримується принципів чистої архітектури та поділений на такі рівні:
* **`models/`**: `dataclasses` (User, Book), які виступають суто структурами даних без складної логіки.
* **`repositories/`**: Відповідають за збереження та отримання даних. Використано інтерфейси (`base.py` з ABC) для абстракції. Реалізовано `InMemoryBookRepository` та `InMemoryUserRepository` для імітації БД.
* **`services/`**: Рівень бізнес-логіки (`library_service.py`). Сервіс нічого не знає про те, *як* зберігаються дані. Він працює виключно з абстрактними репозиторіями та реалізує правила (наприклад, не видавати вже видану книгу).
* **`controllers/`**: CLI-контролер (`cli_controller.py`) є точкою входу. Він приймає запити, звертається до сервісу і форматує вивід (або помилки).

## 3. Рефакторинг та стандартизація (Код-рев'ю)
Під час розробки застосовувався лінтер **`flake8`**.
* **Виявлені "запахи коду" під час ранніх ітерацій:** Жорстка прив'язка сервісу до конкретної бази даних (Coupling) та змішування логіки перевірок з логікою збереження.
* **Рефакторинг:** Було впроваджено Dependency Injection. Тепер `LibraryService` приймає абстрактні репозиторії через конструктор `__init__`. Додано анотації типів (Type Hints) для покращення читабельності коду. Методи збережено компактними (Single Responsibility Principle).

## 4. Інструкції для запуску тестів

### Вимоги:
Переконайтеся, що у вас встановлено Python 3.8+ та бібліотеку `pytest`.
Встановити pytest можна командою:
`pip install pytest`

### Запуск:
Перебуваючи в кореневій папці проєкту, виконайте команду:
`pytest -v`
Прапорець `-v` (verbose) дозволить побачити детальний звіт по кожному з 8 тестів.

### Зразок журналів тестів (Test Logs):
```text
============================= test session starts ==============================
platform darwin -- Python 3.10.12, pytest-7.4.0, pluggy-1.0.0
rootdir: /Users/nst/Desktop/uni/semester 2/analysis/library_project
collected 8 items                                                              

tests/test_library_service.py::test_register_new_user_success PASSED     [ 12%]
tests/test_library_service.py::test_register_user_duplicate_email PASSED [ 25%]
tests/test_library_service.py::test_find_book_by_title PASSED            [ 37%]
tests/test_library_service.py::test_borrow_book_success PASSED           [ 50%]
tests/test_library_service.py::test_borrow_book_invalid_user PASSED      [ 62%]
tests/test_library_service.py::test_borrow_already_borrowed_book PASSED  [ 75%]
tests/test_library_service.py::test_return_book_success PASSED           [ 87%]
tests/test_library_service.py::test_return_not_borrowed_book PASSED      [100%]

============================== 8 passed in 0.04s ===============================