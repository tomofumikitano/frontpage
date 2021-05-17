# vi: ft=dockerfile

FROM python:3.8-slim-buster AS frontpage-base 
ADD requirements.txt .
RUN apt-get update -y && \
		pip install -r requirements.txt && \
		apt-get autoremove -y && \
		rm -rf /var/lib/apt/lists/*


FROM frontpage-base
WORKDIR /app
ADD ./app /app
ENV PYTHONPATH='/app'

ENTRYPOINT ["entrypoint.sh"]
