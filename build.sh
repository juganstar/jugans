#!/usr/bin/env bash
set -o errexit

# Install ONLY what's missing
pip install dj-database-url==2.1.0
pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate