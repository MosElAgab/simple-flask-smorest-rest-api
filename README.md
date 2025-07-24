# Simple Flask Smorest REST API

This is a portfolio project I built to learn and demonstrate real-world skills in backend development, containerization, infrastructure automation, and CI/CD pipelines. It’s a production-like REST API developed with Flask following TDD best practices using pytest, containerized using Docker, deployed on AWS EC2 via Terraform, and integrated with a full CI/CD pipeline using GitHub Actions.

## Features
- CRUD API for Items, Stores, and Tags
- JWT Authentication (with admin role support and token revocation)
- User registration and login
- Integrated unit and integration testing (with pytest)
- Docker & Docker Compose
- PostgreSQL container with persistent volumes
- Deployed on AWS EC2 using Terraform (infrastructure as code)
- Makefile with targets to automate testing, development and deployment tasks
- CI/CD pipelines using GitHub Actions for automated testing and deployment

---

<!-- # Tech -->












<!-- ---
- future develpment: refresh jwt tokens
- furture develpment: consider proper blocklist
# Config todos/considerations
- allow instance folder overrides for pre-dveloper settings ()
- e.g: app = Flask(__name__, instance_relative_configs=True)
- review defaults and add env vairables validations
# First-time setup
cp .env.example .env      # → edit .env with real values

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt
flask run
- test flow
- modesl: unit tests: integration tests
- schema: units tests: integration tests
- services:

![CI](https://github.com/MosElAgab/simple-flask-smorest-rest-api/actions/workflows/ci.yml/badge.svg)

![CI](https://github.com/MosElAgab/simple-flask-smorest-rest-api/.github/workflows/CI.yml/badge.svg) -->
