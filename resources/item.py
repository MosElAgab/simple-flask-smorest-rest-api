from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from db import items, stores
from models import ItemModel
from schema import ItemSchema, ItemUpdateSchema


blp = Blueprint("items", __name__, description="Operations on items")


# /item
# FIXME: item or items
@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        items = ItemModel.query.all()
        return items

    
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message="Database Error: " + str(e.orig))
        return item



# /item/<item_id>
@blp.route("/item/<string:item_id>")
class Store(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        try:
            items[item_id] |= item_data
            return items[item_id]
        except KeyError:
            abort(404, "item not found")