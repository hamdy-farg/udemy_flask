from flask import Flask, request
from db import db 
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError 
import uuid
from models import ItemModel, StoreModel
from schema import ItemSchema, ItemUpdateSchema

blp = Blueprint("Item", __name__, description="CRUD operation on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.arguments(ItemUpdateSchema)
    @blp.response(201, ItemUpdateSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            id_i = uuid.uuid4().hex
            item = ItemModel(id=id_i, **item_data)
        db.session.add(item)
        db.session.commit()
        return item
    
    def delete(self, item_id):   
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "item deleted successfuly"}

    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

@blp.route("/item")
class addItem(MethodView):
    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema)
    def post(self, item_data):
        item = ItemModel.query.filter_by(name=item_data["name"]).first()
        if item:
            abort(400, "this item is created before")
        else:
            item_id = uuid.uuid4().hex
            item = ItemModel(id=item_id,**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, "Error accured while inserting into db")
        return item


@blp.route("/items")
class ItemList(MethodView):
    
    @blp.response(200,ItemSchema(many=True))
    def get(self, ):
            items = ItemModel.query.all()
            return items


