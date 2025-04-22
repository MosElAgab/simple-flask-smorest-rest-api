from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


from db import db
from db import stores
from models import StoreModel
from schema import StoreSchema, StoreUpdateSchema


blp = Blueprint("stores", __name__, description="Operations on stores")


# /store
@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        stores = StoreModel.query.all()
        return stores

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        new_store = StoreModel(**store_data)
        try:
            db.session.add(new_store)
            db.session.commit()
        except IntegrityError as e:
            abort(500, message="Database constraint violated: " + str(e.orig))
        except SQLAlchemyError as e:
            abort(500, message="Database Error: " + str(e.orig))

        return new_store


# /store/<store_id>
@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, "Store not found")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted"}, 200
        except KeyError:
            abort(404, "Store not found")

    @blp.arguments(StoreUpdateSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, store_id):
        try:
            stores[store_id] |= store_data
            return stores[store_id]
        except KeyError:
            abort(404, "Store not found")
