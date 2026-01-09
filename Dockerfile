FROM python:3.13-slim

# Установка Poetry в систему, без виртуальных окружений
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

# Установка системных пакетов и Poetry
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libmagic1 \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем конфиги Poetry
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости (уже в системный Python)
RUN poetry install --no-root --only main

# Копируем весь проект
COPY . .

EXPOSE 8000

# Запуск напрямую через uvicorn (пакеты уже в системном Python)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]