import os 
from flask import Flask
from flask_smorest import Api

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
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL","sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
#connect SQLAlchemy with the flask app

api = Api(app)


from ressources.invoice import blp as InvoiceBluePrint

api.register_blueprint(InvoiceBluePrint)