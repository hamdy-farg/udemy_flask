from flask import Flask, request
from db import db 
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from models.store import StoreModel
from schema import StoreSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import uuid

blp = Blueprint("store", __name__, description="CRUD operation on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
       store = StoreModel.query.get_or_404(store_id)
       return store
        
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "store deleted successufly"}


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        stores = StoreModel.query.all()
        return stores

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        #                  
        store_id = uuid.uuid4().hex
        new_store = StoreModel(id= store_id,**store_data)
        #
        try:
            db.session.add(new_store)
            db.session.commit()
        except IntegrityError:
            abort (400, "problem accured when adding the store to sqflite")
        except SQLAlchemyError:
            abort(500, "the market name is exists before ")
        return new_store 
        

#   for store in stores.values():
#             if store_data["name"] == store["name"] :
#                 abort(400,message=""" Bad request,
#                     your store name is exists
#                     before enter another name """)