
from db import db
class StoreModel(db.Model):
    __tablename__ = "Store"
    id = db.Column(db.String(80), nullable= False, primary_key=True)
    name = db.Column(db.String(80), nullable= False, unique=True)
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic")     