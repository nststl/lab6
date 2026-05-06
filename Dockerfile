# Використовуємо офіційний легкий образ Python
FROM python:3.10-slim

# Встановлюємо робочу директорію всередині контейнера
WORKDIR /app

# Копіюємо файл із залежностями та встановлюємо їх
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код проєкту (папки src, tests та main.py)
COPY . .

# Команда, яка виконається при старті контейнера
CMD ["python", "main.py"]