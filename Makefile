NAME?=serenashah
GID=816966
UID=876392

all: stop-all build-all run-all

images:
	- docker images | grep ${NAME}

ps:
	- docker ps -a | grep ${NAME}

api-stop: 
	docker stop ${NAME}-earthquake-api && docker rm -f ${NAME}-earthquake-api || true

worker-stop:
	docker stop ${NAME}-earthquake-wrk && docker rm -f ${NAME}-earthquake-wrk || true

db-stop:
	docker stop ${NAME}-earthquake-db && docker rm -f ${NAME}-earthquake-db || true

api-build:
	docker build -t ${NAME}/earthquake-api:0.1 -f docker/Dockerfile.api . 

worker-build:
	docker build -t ${NAME}/earthquake-wrk:0.1 -f docker/Dockerfile.wrk .

db-build:
	docker pull redis:6

api-run:
	RIP=$$(docker inspect ${NAME}-db | grep \"IPAddress\" | head -n1 | awk -F\" '{print $$4}') && \
	docker run --name ${NAME}-earthquake-api --env REDIS_IP=${RIP} -d -p 5028:5000 -v \:/earthquake-api ${NAME}/earthquake-api:0.1

worker-run:
	RIP=$$(docker inspect ${NAME}-db | grep \"IPAddress\" | head -n1 | awk -F\" '{print $$4}') && \
	docker run --name ${NAME}-earthquake-wrk --env REDIS_IP=${RIP} -d ${NAME}/earthquake-wrk:0.1

db-run: db-build
	docker run --name ${NAME}-earthquake-db -p 6428:6379 -d -u ${UID}:${GID} -v ${PWD}/src:/src redis:6

stop-all: api-stop worker-stop db-stop

build-all: api-build worker-build db-build

run-all: api-run worker-run db-run
