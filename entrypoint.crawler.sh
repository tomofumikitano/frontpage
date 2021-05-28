#!/usr/bin/env bash
cd app

python manage.py makemigrations
python manage.py migrate

python manage.py runscheduler
