import pytest
import sqlite3
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask_jwt_extended import create_access_token

from app import create_app
from app.db import db
from app.models import UserModel


# enforces fk constraint in sqlite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
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
    "yeilds a fresh db seasson for each test"
    with app.app_context():
        yield db.session
        db.session.remove()


@pytest.fixture
def auth_header(session):
    from app.models import UserModel
    from flask_jwt_extended import create_access_token

    user = UserModel(username="TestUser", password="testpass")
    session.add(user)
    session.commit()

    token = create_access_token(identity=str(user.user_id))
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_auth_header(session):
    from app.models import UserModel
    from flask_jwt_extended import create_access_token

    user = UserModel(username="AdminUser", password="testpass", is_admin=True)
    session.add(user)
    session.commit()

    token = create_access_token(identity=str(user.user_id))
    return {"Authorization": f"Bearer {token}"}
