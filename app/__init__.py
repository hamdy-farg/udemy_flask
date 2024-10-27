from flask import Flask, request
import os

from flask_smorest import Api
from resource.item import blp as ItemBluePrint
from resource.store import blp as StoreBluePrint
from flask_sqlalchemy import SQLAlchemy
from db import db
import models


def create_app(db_url=None):
    
    app = Flask(__name__)
    # flask morest configration
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

    # sqlalchemy configtation
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URI", "sqlite:///data.db")
    app.config['SECRET_KEY'] = '733d791846a024419216029bda1c43ac'    
    app.has_initialized = False
    app.app_context().push()
    db.init_app(app)
    @app.before_request
    def create_tables():
        if not app.has_initialized:
            app.has_initialized = True 
            db.create_all()
    create_tables()
    return app 

app  = create_app()
