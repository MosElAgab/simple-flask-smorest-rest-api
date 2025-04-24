from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


from db import db
from models import StoreModel
from schema import StoreSchema, StoreUpdateSchema, PlainStoreSchema


blp = Blueprint("stores", __name__, description="Operations on stores")


# /store
@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, PlainStoreSchema(many=True))
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
@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id, description="Store not Found")
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}, 200

    @blp.arguments(StoreUpdateSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, store_id):
        store = StoreModel.query.get(store_id)
        if store:
            store.store_name = store_data["store_name"]
        else:
            store = StoreModel(store_id=store_id, **store_data)
            db.session.add(store)
        try:
            db.session.commit()
        except IntegrityError as e:
                abort(500, message="Database constraint violated: " + str(e.orig))
        return store
