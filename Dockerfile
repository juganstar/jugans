# Dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

# Run differently based on environment
CMD if [ "$DJANGO_ENV" = "production" ]; then \
        python manage.py migrate && \
        python manage.py collectstatic --noinput && \
        gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}; \
    else \
        python manage.py runserver 0.0.0.0:8000; \
    fi
