#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies (adjust if using poetry or pipenv)
pip install -r requirements.txt

# Collect static files for production
python manage.py collectstatic --no-input

# Apply migrations to keep DB schema up to date
python manage.py migrate
