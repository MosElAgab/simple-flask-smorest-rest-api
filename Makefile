# Default task
.PHONY: help build-app-container run-app-container run-app test lint format install-req print-req coverage run-app-container-prod migrate terraform-plan terraform-apply terraform-destroy

help:
	@echo "  Note:            ❌ Please activate the virtual environment first."
	@echo "Available commands:"
	@echo "  make build-app-container    - Build the Docker container for the Flask app"
	@echo "  make run-app-container      - Run Flask app in Docker with live mount"
	@echo "  make run-app                - Run the Flask app locally"
	@echo "  make test                   - Run unit tests"
	@echo "  make lint                   - Run linter to check code style"
	@echo "  make format                 - Auto-format code using Black"
	@echo "  make install-req            - Install dependencies from requirements.txt"
	@echo "  make print-req              - Save current dependencies to requirements.txt"

build-app-container:
	docker build -t flask-somrest-rest-api .

run-app-container:
	docker rm -f flask-app || true
	docker run -dp 5007:5000 -w /app -v "$(shell pwd):/app" --name flask-app flask-somrest-rest-api

run-app-container-prod:
	docker rm -f flask-app || true
	docker run -dp 5007:5000 -w /app --env-file .env --name flask-app flask-somrest-rest-api

run-app:
	flask run

test:
	PYTHONPATH=$(shell pwd) pytest -v

coverage:
	PYTHONPATH=$(shell pwd) pytest --cov=app

lint:
	flake8 \
	./test/*.py \
	./test/unit_test/models/*.py \
	./test/integration/*.py \
	./app/__init__.py \
	./app/models/store.py

format:
	black .

install-req:
	pip install -r requirements.txt

print-req:
	pip freeze > requirements.txt

up:
	docker-compose up -d --build

migrate:
	docker-compose exec app flask db upgrade

down:
	docker-compose down -v --remove-orphans

terraform-plan:
	terraform -chdir=terraform-flask-api plan

terraform-apply:
	terraform -chdir=terraform-flask-api apply

terraform-destroy:
	terraform -chdir=terraform-flask-api destroy