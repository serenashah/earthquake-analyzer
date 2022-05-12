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
	docker build -t ${NAME}/earthquake-api:1.0 -f docker/Dockerfile.api . 

worker-build:
	docker build -t ${NAME}/earthquake-wrk:1.0 -f docker/Dockerfile.wrk .

db-build:
	docker pull redis:6

api-run:
	RIP=$$(docker inspect ${NAME}-earthquake-db | grep \"IPAddress\" | head -n1 | awk -F\" '{print $$4}') && \
	docker run --name ${NAME}-earthquake-api --env REDIS_IP=$${RIP} -d -p 5028:5000 ${NAME}/earthquake-api:1.0

worker-run:
	RIP=$$(docker inspect ${NAME}-earthquake-db | grep \"IPAddress\" | head -n1 | awk -F\" '{print $$4}') && \
	docker run --name ${NAME}-earthquake-wrk --env REDIS_IP=$${RIP} -d ${NAME}/earthquake-wrk:1.0

db-run: db-build
	docker run --name ${NAME}-earthquake-db -p 6428:6379 -d -u ${UID}:${GID} -v ${PWD}/data:/data redis:6 --save 1 1

stop-all: api-stop worker-stop db-stop

build-all: db-build api-build worker-build

run-all: db-run api-run worker-run

cycle-api: api-stop api-build api-run

cycle-wrk: worker-stop worker-build worker-run
