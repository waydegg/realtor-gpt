.PHONY: start
start:
	\
		POSTGRES_USER=${POSTGRES_ADMIN_USER} \
		POSTGRES_PASSWORD=${POSTGRES_ADMIN_PASSWORD} \
		uvicorn api.main:app --port 8002

.PHONY: dev
dev:
	\
		POSTGRES_USER=${POSTGRES_ADMIN_USER} \
		POSTGRES_PASSWORD=${POSTGRES_ADMIN_PASSWORD} \
		uvicorn api.main:app --port 8002 --reload

.PHONY: build
build:
	autoflake --remove-all-unused-imports --recursive --in-place src/api
	docker build -t realtor-gpt/api . 

