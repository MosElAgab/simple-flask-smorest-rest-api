# Default task
.PHONY: help build-app-container run-app-container run-app test lint format install

help:
	@echo "  Note:            ❌ Please activate the virtual environment first."
	@echo "Available commands:"
	@echo "  make build-app-container    - Build the Docker container for the Flask app"
	@echo "  make run-app-container      - Run Flask app in Docker with live mount"
	@echo "  make run-app                - Run the Flask app locally"
	@echo "  make test                   - Run unit tests"
	@echo "  make lint                   - Run linter to check code style"
	@echo "  make format                 - Auto-format code using Black"
	@echo "  make install                - Install dependencies from requirements.txt"

build-app-container:
	docker build -t flask-somrest-rest-api .

run-app-container:
	docker run -dp 5006:5000 -w /app -v "$(shell pwd):/app" flask-somrest-rest-api

run-app:
	flask run

test:
	pytest tests/

lint:
	flake8 .

format:
	black .

install:
	pip install -r requirements.txt
