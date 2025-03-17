DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
USER_SERVICE_STORAGE_FILE = docker_compose/user-service-storages.yaml
USER_SERVICE_FILE = docker_compose/user-service.yaml
ENV = --env-file .env
USER_SERVICE_CONTAINER = user-service


.PHONY: user-service-storage
user-service-storage:
	${DC} -f ${USER_SERVICE_STORAGE_FILE} ${ENV} up --build -d

.PHONY: user-service-storage-logs
user-service-storage-logs:
	${DC} -f ${USER_SERVICE_STORAGE_FILE} ${ENV} up --build -d

.PHONY: user-service-storage-down
user-service-storage-down:
	${DC} -f ${USER_SERVICE_STORAGE_FILE} ${ENV} up --build -d

.PHONY: user-service
user-service:
	${DC} -f ${USER_SERVICE_FILE} ${ENV} up --build -d

.PHONY: user-service-down
user-service-down:
	${DC} -f ${USER_SERVICE_FILE} down

.PHONY: user-service-logs
user-service-logs:
	${LOGS} ${USER_SERVICE_CONTAINER} -f


.PHONY: all
all:
	${DC} -f ${USER_SERVICE_STORAGE_FILE} -f ${USER_SERVICE_FILE} ${ENV} up --build -d

.PHONY: all-down
all-down:
	${DC} -f ${USER_SERVICE_STORAGE_FILE} -f ${USER_SERVICE_FILE} down
