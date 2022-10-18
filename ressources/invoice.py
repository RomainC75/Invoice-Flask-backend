from ast import arguments
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request, jsonify

from db import db

from schemas import InvoiceSchema
from models import SenderAddressModel, ClientAddressModel, InvoiceModel, ItemModel, UserModel
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, get_jwt_identity

from datetime import datetime

blp = Blueprint('Invoices', __name__, description="Operations on stores")

@blp.route("/invoice")
class Invoice(MethodView):
    @jwt_required()
    @blp.arguments(InvoiceSchema)
    def post(self, data):
        print(request.headers)
        current_user_id = get_jwt_identity()
        items = data["items"]
        del data["items"]

        clientAddress = ClientAddressModel(**data["clientAddress"])
        db.session.add(clientAddress)
        db.session.commit()
        db.session.refresh(clientAddress)
        clientAddress_id=clientAddress.id
        del data["clientAddress"]
        senderAddress = SenderAddressModel(**data["senderAddress"])
        db.session.add(senderAddress)
        db.session.commit()
        db.session.refresh(senderAddress)
        senderAddress_id=senderAddress.id
        del data["senderAddress"]

        data["senderAddress_id"]=senderAddress_id
        data["clientAddress_id"]=clientAddress_id
        data["createdAt"]=datetime.now()
        data["user_id"]=current_user_id

        invoice = InvoiceModel(**data)
        db.session.add(invoice)
        db.session.commit()
        #get the new id back
        db.session.refresh(invoice)
        invoice_id = invoice.id

        for itemO in items :
            itemO['invoice_id']=invoice_id
            item = ItemModel(**itemO)
            print(item)
            db.session.add(item)
            db.session.commit()

        return data,201

# unprotected
@blp.route('/invoice/<int:invoice_id>')
class Invoice(MethodView):
    @jwt_required()
    @blp.response(200, InvoiceSchema)
    def get(self, invoice_id):
        current_user_id = get_jwt_identity()
        data = InvoiceModel.query.get_or_404(invoice_id)
        print('===> data : ',data)
        return data,200

    def delete(self, invoice_id):
        InvoiceModel.query.filter_by(id=invoice_id).delete()
        db.session.commit()
        return {"message":"invoice deleted!"}
