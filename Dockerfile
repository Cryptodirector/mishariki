# Используем официальный Python образ
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR .

# Копируем файлы с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы вашего приложения в контейнер
COPY . .

# Команда по умолчанию будет запускать обе части приложения
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 5000" && python3 app/backend/tg_bot.py]