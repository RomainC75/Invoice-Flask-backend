from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request

blp = Blueprint('Invoices', __name__, description="Operations on stores")

@blp.route("/invoice")
class Invoice(MethodView):

    def post(self):
        print(request.get_json())
        return "hello",201