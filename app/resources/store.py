from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask_jwt_extended import jwt_required

from app.db import db
from app.models import StoreModel
from app.schemas import StoreSchema, StoreUpdateSchema, PlainStoreSchema


blp = Blueprint("stores", __name__, description="Operations on stores")


# /store
@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, PlainStoreSchema(many=True))
    def get(self):
        stores = StoreModel.query.all()
        return stores

    @jwt_required()
    @blp.arguments(PlainStoreSchema)
    @blp.response(201, PlainStoreSchema)
    def post(self, store_data):
        new_store = StoreModel(**store_data)
        try:
            db.session.add(new_store)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            if "UNIQUE constraint" in str(e.orig):
                abort(409, message="A store with this name already exists.")
            abort(400, message="Database Integrity violated: " + str(e.orig))
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message="Database Error: " + str(e.orig))

        return new_store


# /store/<store_id>
@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
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
                db.session.rollback()
                if "UNIQUE constraint" in str(e.orig):
                    abort(409, message="A store with this name already exists.")
                abort(400, message="Database constraint violated: " + str(e.orig))
        return store
