import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort


from db import items, stores
from schema import ItemSchema, ItemUpdateSchema


blp = Blueprint("items", __name__, description="Operations on items")


# /item
@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()
    
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        # # check valid store id
        if item_data['store_id'] not in stores:
            abort(404, message="Store not found.")
        # ensure no duplicates
        for item in items.values():
            if item["item_name"] == item_data["item_name"] and item["store_id"] == item_data["store_id"]:
                abort(400, message="Bad request, Item already exist.")

        item_id = uuid.uuid4().hex
        new_item = {**item_data, "item_id": item_id}
        items[item_id] = new_item
        return new_item, 200


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