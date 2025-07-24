# Simple Flask Smorest REST API

This is a portfolio project I built to learn and demonstrate real-world skills in backend development, containerization, infrastructure automation, and CI/CD pipelines. It’s a production-like REST API developed with Flask following TDD best practices using pytest, containerized using Docker, deployed on AWS EC2 via Terraform, and integrated with a full CI/CD pipeline using GitHub Actions.











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

![CI](https://github.com/MosElAgab/simple-flask-smorest-rest-api/.github/workflows/CI.yml/badge.svg)
