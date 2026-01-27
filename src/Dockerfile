FROM python:3.14-slim

WORKDIR /src

ENV PYTHONPATH=/src

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Кэшируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# COPY src/api/asgi.py .
# COPY ../alembic.ini .
# COPY ../alembic/ ./alembic/
COPY . .