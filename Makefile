NAME=serenashah

all: build run

images:
	- docker images | grep ${NAME}

ps:
	- docker ps -a | grep ${NAME}

build:
	docker build -t ${NAME}/earthquake-api:0.1 .

run:
	docker run --name "${NAME}-earthquake-api" -d -p 5028:5000 --rm -v \:/earthquake-api ${NAME}/earthquake-api:0.1
