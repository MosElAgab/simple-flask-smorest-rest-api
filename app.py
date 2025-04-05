from flask import Flask
from flask_smorest import Api

from resources.store import blp as StoreBlueprint
from resources.item import blp as ItemBlueprint


app = Flask(__name__)


app.config["PROPOGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "simple-flask-somorest-api"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"


@app.route("/")
def home():
    return "hello, World!"


api = Api(app)


api.register_blueprint(StoreBlueprint)
api.register_blueprint(ItemBlueprint)
