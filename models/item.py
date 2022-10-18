from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    quantity = db.Column(db.Integer())
    price = db.Column(db.Float())
    # invoice = db.relationship("InvoiceModel", back_populates="items")
    invoice_id = db.Column(
        db.Integer, db.ForeignKey("invoices.id"), unique=False, nullable=False
    )
    invoice = db.relationship("InvoiceModel", back_populates="items")