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
	@echo $(DATABASE_URL)
	python3 app/manage.py makemigrations
	python3 app/manage.py migrate

test_db:
	@psql -c "\conninfo" $(DATABASE_URL)

setup_db:
	psql $(DATABASE_URL) -f "scripts/db/setup_postgres.sql"

heroku_test_db:
	@psql -c "\conninfo" $(shell heroku config:get DATABASE_URL)

runscheduler:
	python3 app/manage.py runscheduler

update_feeds:
	python3 app/manage.py update_feeds
