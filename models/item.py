
from db import db
class ItemModel(db.Model):
    __tablename__ = "Item"
    id =db.Column(db.String(80), nullable= False, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    store_id = db.Column(db.String(80), db.ForeignKey("Store.id"), nullable=False)
    store = db.relationship("StoreModel", back_populates="items")
