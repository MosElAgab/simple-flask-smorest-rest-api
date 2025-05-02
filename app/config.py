import os
import secrets

class BaseConfig:
    PROPAGATE_EXCEPTIONS = True
    API_TITLE = "simple-flask-somorest-api"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", str(secrets.SystemRandom().getrandbits(128)))


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev-data.db"


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(BaseConfig):
    PROPOGATE_EXCEPTIONS = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


config_mapping = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}
