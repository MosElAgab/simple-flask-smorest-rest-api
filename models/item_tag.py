from db import db


class ItemTagModel(db.Model):
    __tablename__ = "item_tag"

    item_tag_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.item_id"), unique=False, nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.tag_id"), unique=False, nullable=False)
