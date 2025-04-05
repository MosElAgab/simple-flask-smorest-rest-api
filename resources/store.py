import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort


from db import stores
from schema import StoreSchema, StoreUpdateSchema


blp = Blueprint("stores", __name__, description="Operations on stores")


# /store
@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        if "store_name" not in store_data:
            abort(
                400,
                message="Bas request. Ensure 'store_name' is included"
            )
        for store in stores.values():
            if store["store_name"] == store_data["store_name"]:
                abort(
                    400,
                    message="Store already exists."
                )
        store_id = uuid.uuid4().hex
        new_store = {**store_data, "store_id": store_id}
        stores[store_id] = new_store
        return new_store, 201


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
