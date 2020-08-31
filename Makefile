IMAGE_NAME:=pyslowloris

.PHONY: help

help: ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build-docker:  ## Build docker image locally
	docker build -t $(IMAGE_NAME) .

run-compose:  ## Launch docker compose
	docker-compose up --build -d

stop-compose:  ## Stop docker compose
	docker-compose down

setup-poetry:  ## Install poetry
	pip install poetry
	poetry install

pytest:  ## Launch pytest insdie of poetry env
	poetry run pytest

flake8: ## Launch flake8 insdie of poetry env
	poetry run flake8 ./pyslowloris

isort:  ## Launch isort insdie of poetry env
	poetry run isort -rc ./pyslowloris ./tests
