from flask import Flask, request
from db_data import stores, items
from flask_smorest import abort, Blueprint
from flask.views import MethodView
import uuid
blp = Blueprint("Item", __name__, description="CRUD operation on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
        
    def put(self, item_id):
        request_data = request.get_json()
        try:
            item = items[item_id]
            item |= request_data
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

    def get(self, item_id):
        if items.get(item_id) != None:   
            return {"item" : items[item_id]},200
        else:
            return {"msg": "the item doesnot found"},404

@blp.route("/item")
class addItem(MethodView):
    def post(self):
        item_id = uuid.uuid4().hex
        request_data = request.get_json()
        #
        if ("name" not in request_data and
        "size" not in request_data):
            abort(400,message="Bad Request , Ensure you include name and size")
        #
        items[item_id] = {
            **request_data,
            'id': item_id
            }
        return {"item":items[item_id]}, 201

@blp.route("/items")
class ItemList(MethodView):
    def get(self, ):
            
            return {**items},200


