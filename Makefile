# Default task
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make run         - Run the Flask app"
	@echo "  make test        - Run unit tests"
	@echo "  make lint        - Run linter"
	@echo "  make format      - Auto-format code"
	@echo "  make install     - Install dependencies"

run:
	flask run

test:
	pytest tests/

lint:
	flake8 .

format:
	black .

install:
	pip install -r requirements.txt
