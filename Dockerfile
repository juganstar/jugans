FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install requirements first (caching optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Entrypoint
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Add this for production
CMD ["gunicorn", "your_project.wsgi:application", "--bind", "0.0.0.0:8000"]