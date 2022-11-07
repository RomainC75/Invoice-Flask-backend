from models import SenderAddressModel, ClientAddressModel
from db import db

def update_senderAddress(new_senderAddress , senderAddress_id):
    print("sender address id : ", senderAddress_id)
    senderAddress_to_update = SenderAddressModel.query.get(senderAddress_id)
    senderAddress_to_update.name = new_senderAddress['name']
    senderAddress_to_update.street = new_senderAddress['street']
    senderAddress_to_update.city = new_senderAddress['city']
    senderAddress_to_update.postCode = new_senderAddress['postCode']
    senderAddress_to_update.country = new_senderAddress['country']
    db.session.commit()


def update_clientAddress(new_clientAddress , clientAddress_id):
    print("client address id : ", clientAddress_id)
    senderAddress_to_update = ClientAddressModel.query.get(clientAddress_id)
    senderAddress_to_update.name = new_clientAddress['name']
    senderAddress_to_update.street = new_clientAddress['street']
    senderAddress_to_update.city = new_clientAddress['city']
    senderAddress_to_update.postCode = new_clientAddress['postCode']
    senderAddress_to_update.country = new_clientAddress['country']
    db.session.commit()