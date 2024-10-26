from flask import Flask, request
from db_data import stores, items
from flask_smorest import abort, Blueprint
from flask.views import MethodView
import uuid
from schema import ItemSchema, ItemUpdateSchema

blp = Blueprint("Item", __name__, description="CRUD operation on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.arguments(ItemUpdateSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data
            return {"item": items[item_id]},201
        except KeyError:
            abort(404, "item not found")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "your item deleted"},200
        except KeyError:
            print("heeloo")
            abort(404, msg="your item not found")

    @blp.response(200, ItemSchema)
    def get(self, item_id):
        if items.get(item_id) != None:   
            return {"item" : items[item_id]},200
        else:
            return {"msg": "the item doesnot found"},404

@blp.route("/item")
class addItem(MethodView):
    @blp.arguments(ItemSchema)
    def post(self, item_data):
        item_id = uuid.uuid4().hex
        items[item_id] = {
            **item_data,
            'id': item_id
            }
        return {"item":items[item_id]}, 201

@blp.route("/items")
class ItemList(MethodView):
    
    @blp.response(200,ItemSchema(many=True))
    def get(self, ):
            return items.values()


