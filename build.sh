#!/usr/bin/env bash
set -o errexit

# Critical fix for Render
pip install --upgrade pip
pip install dj-database-url==2.1.0  # Explicit install
pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate