#!make
include .env
export $(shell sed 's/=.*//' .env)

run:
	@export DEBUG=True
	python3 manage.py runserver 0:8000

run_prod:
	python3 manage.py runserver --noreload 0:8000

profile:
	python3 -m cProfile -o profile.cprof manage.py runserver --noreload 0:8000

migrate:
	python3 manage.py makemigrations && python3 manage.py migrate

runscheduler:
	python3 manage.py runscheduler 

update_feeds:
	python3 manage.py update_feeds

test_env:
	@env | grep DB_USER
	@env | grep SECRET_KEY
	@env | grep SQLITE_DB_PATH 
	@env | grep DB_USER
	@env | grep DB_HOST
	@env | grep DB_PORT
