#!make
include .env
export $(shell sed 's/=.*//' .env)

run:
	@export DEBUG=True
	python3 app/manage.py runserver 0:8000

run_prod:
	python3 app/manage.py runserver --noreload 0:8000

profile:
	python3 -m cProfile -o profile.cprof app/manage.py runserver --noreload 0:8000

migrate:
	@env | grep DATABASE_URL 
	python3 app/manage.py makemigrations
	python3 app/manage.py migrate

setup_postgres:
	@env | grep DATABASE_URL 
	psql "postgres://postgres:postgres@192.168.2.107:5432/" -f "scripts/database/setup_postgres.sql"

runscheduler:
	python3 app/manage.py runscheduler 

update_feeds:
	python3 app/manage.py update_feeds

test_env:
	@env | grep SECRET_KEY
	@env | grep DATABASE_URL
