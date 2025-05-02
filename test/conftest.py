import pytest
import sqlite3
from sqlalchemy import event
from sqlalchemy.engine import Engine

from app import create_app
from app.db import db


# enforces fk constraint
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):  # For SQLite only
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


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
