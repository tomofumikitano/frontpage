#!/usr/bin/env bash
cd app

python manage.py makemigrations
python manage.py migrate

python manage.py collectstatic --noinput
python manage.py runserver --noreload 0.0.0.0:$PORT
