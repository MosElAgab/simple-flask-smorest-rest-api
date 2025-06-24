from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required

from app.db import db
from app.models import ItemModel
from app.schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint("items", __name__, description="Operations on items")


# /item
@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        items = ItemModel.query.all()
        return items

    
    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            if "UNIQUE constraint" in str(e.orig):
                abort(409, message="This item already exists in this store.")
            elif "FOREIGN KEY constraint" in str(e.orig):
                abort(409, message="Store referenced does not exist.")
            abort(400, message="Database Integrity violated: " + str(e.orig))
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message="Database Error: " + str(e.orig))
        return item



# /item/<item_id>
@blp.route("/item/<int:item_id>")
class Store(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message":"item deleted"}


    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            for field in ["item_name", "item_price", "store_id"]:
                if field in item_data:
                    setattr(item, field, item_data[field])
        else:
            item = ItemModel(item_id=item_id, **item_data)
            db.session.add(item)

        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            if "UNIQUE constraint" in str(e.orig):
                abort(409, message="This item already exists in this store.")
            elif "FOREIGN KEY constraint" in str(e.orig):
                abort(409, message="Store referenced does not exist.")
            elif "NOT NULL constraint" in str(e.orig):
                abort(
                    409,
                    message="This item does not exist neither can be created due to invalid load"
                )
            abort(400, message="Database Integrity Error: " + str(e.orig))

        return item
