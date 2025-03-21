DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
STORAGES_FILE = docker_compose/storages.yaml
APP_FILE = docker_compose/app.yaml
ENV = --env-file .env
APP_CONTAINER = user-service

.PHONY: storages
user-service-storage:
	${DC} -f ${STORAGES_FILE} ${ENV} up --build -d

.PHONY: storages-down
user-service-storage-down:
	${DC} -f ${STORAGES_FILE} down

.PHONY: app
app:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} down

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: auto-revision
auto-revision:
	${EXEC} ${APP_CONTAINER} alembic revision --autogenerate

.PHONY: revision-upgrade
revision-upgrade:
	${EXEC} ${APP_CONTAINER} alembic upgrade head