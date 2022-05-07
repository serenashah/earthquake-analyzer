NAME?=serenashah

all: api-stop api-build run-all

images:
	- docker images | grep ${NAME}

ps:
	- docker ps -a | grep ${NAME}

api-stop: 
	docker stop ${NAME}-earthquake-api && docker rm -f ${NAME}-earthquake-api || true

worker-stop:
	docker stop ${NAME}-wrk && docker rm -f ${NAME}-earthquake-wrk || true

api-build:
	docker build -t ${NAME}/earthquake-api:0.1 -f docker/Dockerfile.api . 

worker-build:
	docker build -t ${NAME}/earthquake-wrk:0.1 -f docker/Dockerfile.wrk .

api-run:
	RIP=$$(docker inspect ${NAME}-db | grep \"IPAddress\" | head -n1 | awk -F\" '{print $$4}') && \
	docker run --name ${NAME}-earthquake-api --env REDIS_IP=${RIP} -d -p 5028:5000 -v \:/earthquake-api ${NAME}/earthquake-api:0.1

worker-run:
	RIP=$$(docker inspect ${NAME}-db | grep \"IPAddress\" | head -n1 | awk -F\" '{print $$4}') && \
	docker run --name ${NAME}-earthquake-wrk --env REDIS_IP=${RIP} -d ${NAME}/earthquake-wrk:0.1

stop-all: api-stop worker-stop

build-all: api-build worker-build

run-all: api-run worker-run
