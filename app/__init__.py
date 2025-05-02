import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
# import secrets

from .config import config_mapping
from .blocklist import BLOCKLIST
from .db import db
from . import models

from .resources.store import blp as StoreBlueprint
from .resources.item import blp as ItemBlueprint
from .resources.tag import blp as TagBlueprint
from .resources.user import blp as UserBlueprint


def create_app(config_name: str = None, db_url: str = None):

    app = Flask(__name__, instance_relative_config=True)

    # load configs
    config_name = config_name or os.getenv("FLASK_ENV", "development")
    cfg = config_mapping.get(config_name)
    if cfg is None:
        raise ValueError(f"Unknown config: {config_name}")
    app.config.from_object(cfg)

    # for overrides instance/config.py
    app.config.from_pyfile("config.py", silent=True)

    # for db_url overrides
    db_url = db_url or os.getenv("DATABASE_URL")
    if db_url:
        app.config["SQLALCHEMY_DATABASE_URI"] = db_url

    db.init_app(app)

    api = Api(app)

    # how to normally produce a secret key. it should be store it in .env
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def is_admin_claim(identity):
        user = models.UserModel.query.get_or_404(identity)
        return {"is_admin": user.is_admin}

    @jwt.token_in_blocklist_loader
    def check_if_token_terminated(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    # Migration, only wire up when not testing
    if not app.config.get("TESTING"):
        migrate = Migrate()
        migrate.init_app(app, db)

    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    @app.route("/")
    def home():
        return "Hello to Simple-Flask-Smorest-REST-API"

    return app
