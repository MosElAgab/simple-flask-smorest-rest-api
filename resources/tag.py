from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, StoreModel, ItemModel
from schema import TagSchema, PlainTagSchema, ItemSchema, TagAndItemSchema


blp = Blueprint("tags", __name__, description="Operations on tags.")


@blp.route("/store/<string:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        # tag = TagModel.query.get_or_404()
        store = StoreModel.query.get_or_404(store_id)
        return store.tags

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.tag_name == tag_data["tag_name"]).first():
            abort(400, message="A tag with that name already exist in that Store.")
        tag = TagModel(store_id=store_id, **tag_data)
        db.session.add(tag)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message="Error in the database side: " + str(e))
        return tag
    

@blp.route("/tag")
class TagList(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self):
        tags = TagModel.query.all()
        return tags


@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp.response(200, PlainTagSchema)
    def get(self, tag_id):
        tag =TagModel.query.get_or_404(tag_id)
        return tag
    
    @blp.response(
        202,
        description="Deletes a tag if no item is tagged with it.",
        example={"message": "Tag deleted."},
    )
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(
        400,
        description="Returned if the tag is assigned to one or more items. In this case, the tag is not deleted.",
    )
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}
        abort(
            400,
            message="Could not delete tag. Make sure tag is not associated with any items, then try again.",  # noqa: E501
        )


@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class ItemTag(MethodView):
    # TODO: what if the tag attached is not in the same store as the model
    @blp.response(201, ItemSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message="Database Error: " + str(e))
        return item
    
    @blp.response(200, TagAndItemSchema)
    def delete(sefl, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        try:
            item.tags.remove(tag)
            db.session.commit()
        except ValueError as e:
            abort(500, message="Database Error: " + str(e))
        except SQLAlchemyError as e:
            abort(500, message="Database Error: " + str(e))
        
        message = "Tag was unlinked from item successfully"
        
        return {"message": message, "tag": tag, "item": item}