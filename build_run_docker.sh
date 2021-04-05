#!/usr/bin/env bash
IMAGE_NAME=frontpage:v1
CONTAINER_NAME=frontpage
PORT=8000

version=$(git log -n1 --format="%h")

docker container stop $CONTAINER_NAME
docker container rm $CONTAINER_NAME
yes | docker system prune

docker build -f Dockerfile --build-arg version="$version" -t "$IMAGE_NAME" .

docker run -d \
	--restart=always \
	-p $PORT:8000 \
	--name $CONTAINER_NAME \
	--user 1000:1000 \
	$IMAGE_NAME
