# vi: ft=dockerfile

FROM python:3.8-slim-buster AS frontpage-base 
ADD requirements.txt .
RUN apt-get update -y && \
		pip install -r requirements.txt && \
		apt-get autoremove -y && \
		rm -rf /var/lib/apt/lists/*


FROM frontpage-base
WORKDIR /app
ADD app /app
ARG version
ENV APP_VERSION=${version}
ENV PYTHONPATH='/app'
EXPOSE 8000
ENV DB_ENGINE=django.db.backends.sqlite3
ENV DB_NAME=/data/frontpage.sqlite3
CMD ["/usr/local/bin/python", "manage.py", "makemigrations"]
CMD ["/usr/local/bin/python", "manage.py", "migrate"]
CMD ["/usr/local/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]
