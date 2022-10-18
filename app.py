import os 
from db import db
from flask import Flask
from flask_smorest import Api
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

import sys
print('It is working',file=sys.stderr)



load_dotenv()

app = Flask(__name__)

#let see errors in dependancies
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
#standard for API documentation (flask_morest)
app.config["OPENAPI_VERSION"] = "3.0.3"
#tell flask-morest where the root of API is
# ==> http://localhost:5000/swagger-ui !!
app.config["OPENAPI_URL_PREFIX"] = "/"
#tell flask-morest to use swagger for API docu
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
# tell flask-morest to get the code for the docu at this address
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("AWS_URL","sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
#connect SQLAlchemy with the flask app
db.init_app(app)
migrate=Migrate(app,db)



api = Api(app)

app.config["JWT_SECRET_KEY"] = "280601218860886714758979442484081064733"
jwt = JWTManager(app)

from ressources.invoice import blp as InvoiceBluePrint
from ressources.user import blp as UserBluePrint
#no longer needed since flask-migrate has been introduced
# @app.before_first_request
# def create_tables():
#     db.create_all()

api.register_blueprint(InvoiceBluePrint)
api.register_blueprint(UserBluePrint)
