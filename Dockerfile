# Используем готовый образ с Chrome и драйвером
FROM selenium/standalone-chrome:latest

# Настройки для тестов
ENV HEADLESS=true

# Устанавливаем Python
USER root
RUN apt-get update && apt-get install -y python3 python3-pip
RUN ln -s /usr/bin/python3 /usr/bin/python

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . /app
WORKDIR /app

# Запуск тестов
CMD ["python", "-m", "pytest", "tests/", "-v"]