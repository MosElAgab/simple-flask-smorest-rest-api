# Simple Flask Smorest REST API

This is a portfolio project I built to learn and demonstrate real-world skills in backend development, containerization, infrastructure automation, and CI/CD pipelines. It’s a production-like REST API developed with Flask following TDD best practices using pytest, containerized using Docker, deployed on AWS EC2 via Terraform, and integrated with a full CI/CD pipeline using GitHub Actions.

---
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

## Tech Stack

| **Category**               | **Tools / Frameworks**                    |
| -------------------------- | ----------------------------------------- |
| **Backend**                | Python, Flask, Flask-Smorest, Marshmallow |
| **Authentication**         | JWT (via flask-jwt-extended)              |
| **Database**               | PostgreSQL 16.1 (Dockerized)              |
| **ORM**                    | SQLAlchemy                                |
| **Testing**                | Pytest, Coverage.py                       |
| **Containerization**       | Docker, Docker Compose                    |
| **CI/CD**                  | GitHub Actions                            |
| **Infrastructure as Code** | Terraform                                 |
| **Hosting**                | AWS EC2 (Amazon Linux 2023)               |

---

## Project Structure

```bash
.
├── Dockerfile
├── LICENSE
├── Makefile
├── README.md
├── app
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-311.pyc
│   │   ├── blocklist.cpython-311.pyc
│   │   ├── config.cpython-311.pyc
│   │   ├── db.cpython-311.pyc
│   │   └── schema.cpython-311.pyc
│   ├── blocklist.py
│   ├── config.py
│   ├── db.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-311.pyc
│   │   │   ├── item.cpython-311.pyc
│   │   │   ├── item_model.cpython-311.pyc
│   │   │   ├── item_tag.cpython-311.pyc
│   │   │   ├── item_tag_model.cpython-311.pyc
│   │   │   ├── store.cpython-311.pyc
│   │   │   ├── store_model.cpython-311.pyc
│   │   │   ├── tag.cpython-311.pyc
│   │   │   ├── tag_model.cpython-311.pyc
│   │   │   ├── user.cpython-311.pyc
│   │   │   └── user_model.cpython-311.pyc
│   │   ├── item_model.py
│   │   ├── item_tag_model.py
│   │   ├── store_model.py
│   │   ├── tag_model.py
│   │   └── user_model.py
│   ├── resources
│   │   ├── __pycache__
│   │   │   ├── item.cpython-311.pyc
│   │   │   ├── store.cpython-311.pyc
│   │   │   ├── tag.cpython-311.pyc
│   │   │   └── user.cpython-311.pyc
│   │   ├── item.py
│   │   ├── store.py
│   │   ├── tag.py
│   │   └── user.py
│   └── schemas
│       ├── __init__.py
│       ├── __pycache__
│       │   ├── __init__.cpython-311.pyc
│       │   ├── all_schema.cpython-311.pyc
│       │   ├── item_schema.cpython-311.pyc
│       │   ├── shared_schema.cpython-311.pyc
│       │   ├── store_schema.cpython-311.pyc
│       │   ├── tag_schema.cpython-311.pyc
│       │   └── user_schema.cpython-311.pyc
│       ├── item_schema.py
│       ├── shared_schema.py
│       ├── store_schema.py
│       ├── tag_schema.py
│       └── user_schema.py
├── commands_notes.md
├── docker-compose.yml
├── instance
├── migrations
│   ├── README
│   ├── __pycache__
│   │   └── env.cpython-311.pyc
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       ├── __pycache__
│       │   ├── a9241f9fc0a8_.cpython-311.pyc
│       │   └── bf194dabcad1_.cpython-311.pyc
│       ├── a9241f9fc0a8_.py
│       └── bf194dabcad1_.py
├── requirements.txt
├── setup.cfg
├── terraform-flask-api
│   ├── main.tf
│   ├── provider.tf
│   ├── terraform.tfstate
│   └── terraform.tfstate.backup
└── test
    ├── __pycache__
    │   └── conftest.cpython-311-pytest-8.3.5.pyc
    ├── conftest.py
    ├── integration
    │   ├── __pycache__
    │   │   └── test_factory.cpython-311-pytest-8.3.5.pyc
    │   ├── models
    │   │   ├── __pycache__
    │   │   │   ├── test_item_crud.cpython-311-pytest-8.3.5.pyc
    │   │   │   ├── test_item_integraion.cpython-311-pytest-8.3.5.pyc
    │   │   │   ├── test_store.cpython-311-pytest-8.3.5.pyc
    │   │   │   ├── test_store_integration.cpython-311-pytest-8.3.5.pyc
    │   │   │   ├── test_store_model.cpython-311-pytest-8.3.5.pyc
    │   │   │   ├── test_tag_crud.cpython-311-pytest-8.3.5.pyc
    │   │   │   ├── test_tag_integration.cpython-311-pytest-8.3.5.pyc
    │   │   │   └── test_user_integraion.cpython-311-pytest-8.3.5.pyc
    │   │   ├── test_item_integraion.py
    │   │   ├── test_store_integration.py
    │   │   ├── test_tag_integration.py
    │   │   └── test_user_integraion.py
    │   ├── resources
    │   │   ├── __pycache__
    │   │   │   ├── test_item.cpython-311-pytest-8.3.5.pyc
    │   │   │   ├── test_store.cpython-311-pytest-8.3.5.pyc
    │   │   │   ├── test_tag.cpython-311-pytest-8.3.5.pyc
    │   │   │   └── test_user.cpython-311-pytest-8.3.5.pyc
    │   │   ├── test_item.py
    │   │   ├── test_store.py
    │   │   ├── test_tag.py
    │   │   └── test_user.py
    │   └── test_factory.py
    └── unit_test
        ├── models
        │   ├── __pycache__
        │   │   ├── test_item.cpython-311-pytest-8.3.5.pyc
        │   │   ├── test_item_tag_model.cpython-311-pytest-8.3.5.pyc
        │   │   ├── test_item_tag_unit.cpython-311-pytest-8.3.5.pyc
        │   │   ├── test_item_unit.cpython-311-pytest-8.3.5.pyc
        │   │   ├── test_store_model.cpython-311-pytest-8.3.5.pyc
        │   │   ├── test_store_unit.cpython-311-pytest-8.3.5.pyc
        │   │   ├── test_tag_model.cpython-311-pytest-8.3.5.pyc
        │   │   ├── test_tag_unit.cpython-311-pytest-8.3.5.pyc
        │   │   ├── test_user_model.cpython-311-pytest-8.3.5.pyc
        │   │   └── test_user_unit.cpython-311-pytest-8.3.5.pyc
        │   ├── test_item_tag_unit.py
        │   ├── test_item_unit.py
        │   ├── test_store_unit.py
        │   ├── test_tag_unit.py
        │   └── test_user_unit.py
        ├── schemas
        │   ├── __pycache__
        │   │   ├── test_item_schema.cpython-311-pytest-8.3.5.pyc
        │   │   ├── test_shared_schema.cpython-311-pytest-8.3.5.pyc
        │   │   ├── test_store_schema.cpython-311-pytest-8.3.5.pyc
        │   │   ├── test_tag_schema.cpython-311-pytest-8.3.5.pyc
        │   │   └── test_user_schema.cpython-311-pytest-8.3.5.pyc
        │   ├── test_item_schema.py
        │   ├── test_shared_schema.py
        │   ├── test_store_schema.py
        │   ├── test_tag_schema.py
        │   └── test_user_schema.py
        └── services
```










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
