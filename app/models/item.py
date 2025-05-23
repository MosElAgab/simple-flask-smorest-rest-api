from app.db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    __table_args__ = (
        db.UniqueConstraint("item_name", "store_id", name="uq_item_store"),
    )

    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(80), unique=False, nullable=False)
    item_price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.store_id"), unique=False, nullable=False)

    store = db.relationship("StoreModel", back_populates="items")
    tags = db.relationship("TagModel", back_populates="items", secondary="item_tag")
