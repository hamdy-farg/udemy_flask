from flask import Flask, request
from db_data import stores
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from schema import StoreSchema

import uuid

blp = Blueprint("store", __name__, description="CRUD operation on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        if stores.get(store_id)  != None :
            return  stores[store_id]
        else:
            return {"msg": "the store doesnot found"},404
        
    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "your store deleted"},200
        except KeyError:
            abort(404, msg="your store not found")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        if len(stores) != 0:
            
            return  stores.values()
        else :
            abort(404, message="there is no store until now")

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        #       
        for store in stores.values():
            if store_data["name"] == store["name"] :
                abort(400,message=""" Bad request,
                    your store name is exists
                    before enter another name """)
            
        store_id = uuid.uuid4().hex
        new_store = {
        **store_data, "id": store_id
        }
        #
        stores[store_id] = new_store
        return new_store 
        