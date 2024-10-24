from flask import Flask, request
from db_data import stores
from flask_smorest import abort, Blueprint
from flask.views import MethodView

import uuid

blp = Blueprint("store", __name__, description="CRUD operation on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):

    def get(self, store_id):
        if stores.get(store_id)  != None :
            return {"store":stores[store_id]},200
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
    def get(self):
        if len(stores) != 0:
            
            return {"Stores": list(stores.values())}   
        else :
            abort(404, message="there is no store until now")

    def post(self):
        request_data = request.get_json()
        #
        if ("name" not in request_data and
            "seller_name" not in request_data and
            "seller_id" not in request_data):

            abort(400, message="""Bad request,
                Ensure name , seller_name and
                seller_id is included in your pyload""")
        for store in stores.values():
            if request_data["name"] == store["name"] :
                abort(400,message="""Bad request,
                    your store name is exists
                    before enter another name """)
            
        store_id = uuid.uuid4().hex
        new_store = {
        **request_data, "id": store_id
        }
        #
        stores[store_id] = new_store
        return new_store , 201
        