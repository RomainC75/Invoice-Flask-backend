from db import db
from datetime import datetime

class InvoiceModel(db.Model):
    __tablename__ = "invoices"
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False)
    # createdAt = db.Column(db.String(80), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    paymentDue = db.Column(db.DateTime)
    description= db.Column(db.String(300), nullable=False)
    paymentTerms= db.Column(db.Integer)
    clientName= db.Column(db.String(80), nullable=False)
    clientEmail= db.Column(db.String(80), nullable=False)
    status= db.Column(db.String(15), nullable=False)

    items = db.relationship("ItemModel", back_populates="invoice", lazy="dynamic")
    
    senderAddress_id = db.Column(
        db.Integer, db.ForeignKey("senderAddresses.id"), unique=False, nullable=False
    )
    senderAddress = db.relationship("SenderAddressModel", back_populates="invoices")

    clientAddress_id = db.Column(
        db.Integer, db.ForeignKey("clientAddresses.id"), unique=False, nullable=False
    )
    clientAddress = db.relationship("ClientAddressModel", back_populates="invoices")

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False)
    user = db.relationship("UserModel", back_populates = "invoices")
    
    

