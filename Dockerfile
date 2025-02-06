# Используем базовый образ Python
FROM python:3.9-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    unzip \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Установка Google Chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb || apt-get -fy install

# Установка ChromeDriver
RUN CHROMEDRIVER_VERSION=$(curl -sS https://getwebdriver.com/chromedriver#stable) && \
    wget -q "https://storage.googleapis.com/chrome-for-testing-public/133.0.6943.53/linux64/chrome-linux64.zip" && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver && \
    rm chromedriver_linux64.zip


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
