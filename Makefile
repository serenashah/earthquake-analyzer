NAME?=serenashah

all: stop build run

images:
	- docker images | grep ${NAME}

ps:
	- docker ps -a | grep ${NAME}

stop: 
	docker stop ${NAME}-earthquake-api && docker rm -f ${NAME}-earthquake-api || true
build:
	docker build -t ${NAME}/earthquake-api:0.1 -f docker/Dockerfile.api . 

run:
	docker run --name "${NAME}-earthquake-api" -d -p 5028:5000 -v \:/earthquake-api ${NAME}/earthquake-api:0.1
