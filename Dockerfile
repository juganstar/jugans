FROM python:3.11-slim

ENV DJANGO_SETTINGS_MODULE=config.settings
ENV PYTHONPATH="/app"

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
