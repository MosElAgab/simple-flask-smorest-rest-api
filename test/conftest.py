import pytest
from app import create_app
from app.db import db


@pytest.fixture()
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def session(app):
    "yeilds a fress db seasson for each test"
    with app.app_context():
        yield db.session
        db.session.remove()
