from ast import arguments
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request, jsonify
from sqlalchemy import text
from db import db
from sqlalchemy import update
from schemas import InvoiceSchema
from models import SenderAddressModel, ClientAddressModel, InvoiceModel, ItemModel, UserModel
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, get_jwt_identity, decode_token

from datetime import datetime

from db import engine

blp = Blueprint('Invoices', __name__, description="Operations on stores")

val=1

@blp.route('/test/')
class Invoice(MethodView):
    def get(self):
        global val
        val+=1
        return {"message":val},200

@blp.route("/invoice/")
class Invoice(MethodView):
    @blp.response(200,InvoiceSchema(many=True))
    @jwt_required()    
    def get(self):    
        current_user = get_jwt_identity()
        #store = StoreModel.query.get_or_404(int(store_id))
        res = InvoiceModel.query.filter(InvoiceModel.user_id==current_user)
        return res



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
        # current_user_id = 1
        invoice = InvoiceModel.query.get_or_404(invoice_id)
        if(invoice.user_id!=current_user_id):
            abort(400, message = "you don't have the right to get this invoice !")
        return invoice,200

    @jwt_required()
    @blp.arguments(InvoiceSchema)
    @blp.response(200, InvoiceSchema)
    def put(self, invoice_data, invoice_id):
        
        current_user_id = get_jwt_identity()
        print("new : ", invoice_data['items'])
       
        oldInvoice = InvoiceModel.query.get_or_404(invoice_id)
        print(f'==> OLD : {oldInvoice}')
        if(oldInvoice.user_id != current_user_id):
            abort(400, message = "you don't have the right to update this invoice !")
        #=======Items ========
        # create new items which have no Id
        for i, newItem in enumerate(invoice_data['items']):
            if( 'id' not in newItem.keys()):
                print(f'==> very new  //  i : {i} , {newItem}')
                #ADD NEW
                
                with engine.connect() as conn:
                    ans = conn.execute(text(f" INSERT INTO `items` (`name`, `price`, `quantity`, `invoice_id`) VALUES ('{newItem['name']}', '{newItem['price']}', '{newItem['quantity']}', '{oldInvoice.id}' )   " ))
                    print( "ANS : " , ans.__dict__.keys() )

                #remove in the list
                invoice_data['items']= [ item for j, item in enumerate(invoice_data['items']) if j!=i ]


        print("filtered : ",invoice_data['items'])

        # remove items in the db !
        for oldItem in list(oldInvoice.items):
            print('iteration : ' , oldItem.id , [ newItem['id'] for newItem in invoice_data['items'] if 'id' in newItem.keys() ])
            if oldItem.id not in [ newItem['id'] for newItem in invoice_data['items'] if 'id' in newItem.keys() ]  :
                print(f'==> {oldItem.id} has to be removed ')
                #REMOVE FROM DB
                with engine.connect() as conn:
                    ans = conn.execute(text(f"DELETE FROM `items` WHERE `id`='{oldItem.id}'"))

        # update items
        for itemToUpdate in list(invoice_data['items']):
            print(f'update : {itemToUpdate}')
            #UPDATE ITEM
            if 'id' in itemToUpdate:
                with engine.connect() as conn:
                    ans = conn.execute(text(f" UPDATE `items` SET `name`='{itemToUpdate['name']}',`price`='{itemToUpdate['price']}',`quantity`='{itemToUpdate['quantity']}' WHERE `id`='{itemToUpdate['id']}' "))
                    print( "ANS : " , ans.__dict__.keys() )

        del invoice_data['items']

        #=======sender address ========
        senderAddress = invoice_data['senderAddress']
        print("sender address : ", senderAddress)
        
        address=SenderAddressModel(**senderAddress)
        # print("address.items", address.items)
        print("===========================================")
        # db.session.query(SenderAddressModel).filter(SenderAddressModel.id==oldInvoice.senderAddress.id).update(address)
        
        with engine.connect() as conn:
            ans = conn.execute(text(f"UPDATE `senderAddresses` SET `name`='{senderAddress['name']}',`street`='{senderAddress['street']}',`city`='{senderAddress['city']}',`postCode`='{senderAddress['postCode']}',`country`='{senderAddress['country']}' WHERE `id`='{oldInvoice.senderAddress.id}'"))
            print("ANS : ", ans.__dict__.keys())

        # db.session.add(address)
        # db.session.commit()
        
        del invoice_data['senderAddress']
        

        #=======client address ========
        clientAddress = invoice_data['clientAddress']
        print("client address : ", clientAddress)
        address=ClientAddressModel(**clientAddress)
        with engine.connect() as conn:
            ans = conn.execute(text(f"UPDATE `clientAddresses` SET `name`='{senderAddress['name']}',`street`='{senderAddress['street']}',`city`='{senderAddress['city']}',`postCode`='{senderAddress['postCode']}',`country`='{senderAddress['country']}' WHERE `id`='{oldInvoice.senderAddress.id}'"))
            print("ANS : ", ans.__dict__.keys())
        del invoice_data['clientAddress']
        # db.session.add(address)
        # db.session.commit()

        print("rest of the data : ", invoice_data)


        # invoice=InvoiceModel(id=invoice_id,**invoice_data)
        # db.session.add(invoice)
        # db.sesson.commit()
        return oldInvoice










    @jwt_required()
    def delete(self, invoice_id):
        current_user_id = get_jwt_identity()
        invoice = InvoiceModel.query.get_or_404(invoice_id)
        if(invoice.user_id!=current_user_id):
            abort(400, message = "you don't have the right to delete this invoice !")
        InvoiceModel.query.filter_by(id=invoice_id).delete()
        db.session.commit()
        return {"message":"invoice deleted!"}

