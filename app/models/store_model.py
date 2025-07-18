from app.db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    store_id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(80), unique=True, nullable=False)

    items = db.relationship(
        "ItemModel",
        back_populates="store",
        lazy="dynamic",
        cascade="all, delete, delete-orphan"
    )
    tags = db.relationship(
        "TagModel",
        back_populates="store",
        lazy="dynamic",
        cascade="all, delete, delete-orphan"
    )
