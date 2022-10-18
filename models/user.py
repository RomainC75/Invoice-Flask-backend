from db import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(), nullable=False)
    avatar_url = db.Column(db.String())

    # invoice_id = db.Column(db.Integer, db.ForeignKey("invoices.id") )
    # invoices = db.relationship("InvoiceModel", back_populates="invoices" )
    invoices = db.relationship("InvoiceModel", back_populates="user" )
    