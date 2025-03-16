DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
USER_SERVICE_FILE = docker_compose/user_service.yaml
ENV_FILE = .env
USER_SERVICE_CONTAINER = user_service

.PHONY: user-service
user-service:
	${DC} -f ${USER_SERVICE_FILE} --env-file ${ENV_FILE} up --build -d

.PHONY: user-service-down
user-service-down:
	${DC} -f ${USER_SERVICE_FILE} down

.PHONY: user-service-logs
user-service-logs:
	${LOGS} ${USER_SERVICE_CONTAINER} -f
