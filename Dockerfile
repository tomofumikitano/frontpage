# vi: ft=dockerfile

FROM python:3.8-slim-buster AS frontpage-base 
COPY ./requirements.txt /
RUN apt-get update -y && \
		pip install -r requirements.txt && \
		apt-get autoremove -y && \
		rm -rf /var/lib/apt/lists/*

FROM frontpage-base
COPY ./app /app
COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENV PYTHONPATH='/app'

ENTRYPOINT ["/entrypoint.sh"]
