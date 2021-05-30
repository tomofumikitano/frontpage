# vi: ft=dockerfile

FROM python:3.8-slim-buster AS frontpage-base 
COPY ./requirements.txt /
RUN apt-get update -y && \
		apt install -y --no-install-recommends gcc libpq-dev python3-dev && \
		pip install -r requirements.txt && \
		apt -y remove gcc python3-dev && \
		apt-get autoremove -y && \
		rm -rf /var/lib/apt/lists/*

FROM frontpage-base
COPY ./app /app

COPY ./entrypoint.web.sh /
RUN chmod +x /entrypoint.web.sh

COPY ./entrypoint.crawler.sh /
RUN chmod +x /entrypoint.crawler.sh

ENV PYTHONPATH='/app'
