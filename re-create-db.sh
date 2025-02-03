#!/bin/sh

. ".venv/bin/activate"

rm -rf db.sqlite3 restaurant/migrations/*.py
python manage.py makemigrations
python manage.py makemigrations restaurant
python manage.py migrate
