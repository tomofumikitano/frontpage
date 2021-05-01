# vi: ft=dockerfile

FROM python:3.8-slim-buster AS frontpage-base 
ADD requirements.txt .

RUN apt-get update -y && \
		apt install -y --no-install-recommends gcc libpq-dev python3-dev && \
		pip install -r requirements.txt && \
		apt -y remove gcc python3-dev && \
		apt-get autoremove -y && \
		rm -rf /var/lib/apt/lists/*


FROM frontpage-base
WORKDIR /app
ADD app /app
ARG version
ENV APP_VERSION=${version}
ENV PYTHONPATH='/app'
EXPOSE 8000
CMD ["/usr/local/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]
