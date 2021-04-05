# vi: ft=dockerfile

FROM python:3.8-slim-buster AS frontpage-base 
ADD requirements.txt .
RUN apt-get update -y && \
		pip install -r requirements.txt && \
		pip uninstall -y pip && \
		apt-get autoremove -y

FROM frontpage-base
WORKDIR /app
ADD app /app
ARG version
ENV APP_VERSION=${version}
ENV PYTHONPATH='/app'
EXPOSE 8000
CMD ["/bin/bash", "run.sh"]
