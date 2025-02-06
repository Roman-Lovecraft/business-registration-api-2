# Используем официальный базовый образ Python
FROM python:3.9-slim

# Установка зависимостей для Chrome и chromedriver
RUN apt-get update && apt-get install -y wget unzip \
    wget \
    unzip \
    libnss3 \
    libgconf-2-4 \
    gnupg \
    curl \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

# Установка Chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb || apt-get -fy install

# Установка ChromeDriver (версию нужно проверить перед установкой)
RUN CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget -q "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver




# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт для uvicorn
EXPOSE 8000

# Команда для запуска API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
