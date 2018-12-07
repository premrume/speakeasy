#!/bin/sh

docker-compose build
docker images
docker-compose up -d
docker-compose images
#docker-compose stop ui
#docker-compose rm ui
#docker-compose build ui
#docker-compose up -d ui
