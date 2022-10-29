from db import db


#MANY TO MANY
class ClientAddressModel(db.Model):
    __tablename__ = 'clientAddresses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    street = db.Column(db.String(80))
    city = db.Column(db.String(80))
    postCode = db.Column(db.String(80))
    country = db.Column(db.String(80))
    invoices = db.relationship("InvoiceModel", back_populates="clientAddress", lazy="dynamic")