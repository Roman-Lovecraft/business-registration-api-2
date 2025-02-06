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

# Добавление репозитория Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    DISTRO=$(lsb_release -c | awk '{print $2}') && \
    echo "deb [signed-by=/usr/share/keyrings/google-archive-keyring.gpg] https://dl.google.com/linux/chrome/deb/ $DISTRO main" | tee /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update

# Установка Google Chrome версии 114.0.5735.90
RUN apt-get install -y google-chrome-stable=114.0.5735.90-1

# Установка ChromeDriver 114.0.5735.90
RUN wget -q "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip" && \
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
