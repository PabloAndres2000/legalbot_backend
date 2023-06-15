.DEFAULT_GOAL := help

.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: bash
bash: ## enter to backend container
	@docker exec -ti legalbot_backend /bin/bash

## run the project for local development
.PHONY: up
up:
	@docker-compose -f docker-compose.yml up -d --remove-orphans

.PHONY: stop
stop: ## stop Docker containers without removing them
	@docker-compose stop

.PHONY: down
down: ## stop and remove Docker containers
	@docker-compose down --remove-orphans

.PHONY: build
build: ## rebuild base Docker images
	@docker-compose down --remove-orphans
	@docker-compose build --no-cache