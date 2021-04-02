.PHONY: setup deps docker up lint
.DEFAULT_GOAL := help

setup:  ## Install dependencies
	poetry install

deps:  ## Update dependencies
	poetry update

docker:  ## Build the docker images.
	docker build -f Dockerfile -t stellar-server:latest .

up: lint docker  ## Run docker-compose up.
	docker-compose -f docker-compose.yaml up

lint:  ## Run black, isort, mypy
	poetry run black .
	poetry run isort .
	poetry run mypy .

help:  ## Print Make usage information
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort
