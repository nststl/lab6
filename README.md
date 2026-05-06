# Система управління бібліотекою

[![CI/CD Pipeline](https://github.com/nststl/one/actions/workflows/ci.yml/badge.svg)](https://github.com/nststl/one/actions/workflows/ci.yml)

## Запуск через Docker
Щоб запустити додаток разом із базою даних PostgreSQL, виконайте команду:
`docker-compose up -d`

Щоб увійти в інтерактивний режим CLI-додатку всередині контейнера:
`docker exec -it python_library_app python main.py`

### Змінні середовища
Параметри підключення до БД налаштовуються динамічно у `docker-compose.yaml`:
* `DB_HOST`: Хост бази даних (за замовчуванням `postgres_db`)
* `DB_PORT`: Порт (за замовчуванням `5432`)
* `DB_USER` / `DB_PASSWORD`: Логін та пароль бази даних.

## Тестування
Юніт-тести покривають сервісний шар додатка (видачу, повернення та пошук книг).
Для ручного запуску тестів:
`pytest -v tests/`

Тести також автоматично запускаються при кожному коміті завдяки GitHub Actions (див. бейдж статусу зверху).

## Оновлення github
git add README.md
git commit -m "Update README with Docker instructions and CI badge"
git push