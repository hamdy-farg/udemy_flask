from flask import Flask, request
from db_data import stores, items
from flask_smorest import Api
from resource.item import blp as ItemBluePrint
from resource.store import blp as StoreBluePrint
 
app = Flask(__name__)
app.config['PROPAGATE_EXCEPTION'] = True
app.config["API_TITLE"] = "UDEMY REST API"
app.config["API_VERSION"]="v1.0"
app.config["OPENAPI_VERSION"] = '3.0.3'
app.config["OPENAPI_URL_PREFIX"] = '/'
app.config["OPENAPI_SWAGGER_UI_PATH"] = '/swagger'
app.config["OPENAPI_SWAGGER_UI_URL"] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

api =Api(app)

api.register_blueprint(StoreBluePrint)
api.register_blueprint(ItemBluePrint)






if __name__ == '__main__': 
    app.run(debug=True, port=5000)

