#!make
include .env
export $(shell sed 's/=.*//' .env)

run:
	python3 manage.py runserver 0:8000

migrate:
	python3 manage.py makemigrations && python3 manage.py migrate

runscheduler:
	python3 manage.py runscheduler 

update_feeds:
	python3 manage.py update_feeds

test_env:
	@env | grep DB_USER
	@env | grep SECRET_KEY
	@env | grep DB_ENGINE
	@env | grep DB_NAME
	@env | grep DB_USER
	@env | grep DB_HOST
	@env | grep DB_PORT
