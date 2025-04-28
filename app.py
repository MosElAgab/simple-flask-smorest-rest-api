import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
# import secrets

from blocklist import BLOCKLIST
from db import db
import models

from resources.store import blp as StoreBlueprint
from resources.item import blp as ItemBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint

def create_app(db_url=None):
    app = Flask(__name__)


    app.config["PROPOGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "simple-flask-somorest-api"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    
    db.init_app(app)

    api = Api(app)

    # how to normally produce a secret key. it should be store it in .env
    # secret_key = secrets.SystemRandom().getrandbits(128)
    app.config["JWT_SECRET_KEY"] = "mostafa"
    jwt = JWTManager(app)
    
    @jwt.additional_claims_loader
    def is_admin_claim(identity):
        user = models.UserModel.query.get_or_404(identity)
        return {"is_admin": user.is_admin}
    
    @jwt.token_in_blocklist_loader
    def check_if_token_terminated(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
    
    @jwt.additional_claims_loader
    def is_admin_claim(identity):
        user = models.UserModel.query.get_or_404(identity)
        return {"is_admin": user.is_admin}
    
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

    with app.app_context():
        db.create_all()

    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)
    
    
    @app.route("/")
    def home():
        return "Hello to Simple-Flask-Smorest-REST-API"

    return app
