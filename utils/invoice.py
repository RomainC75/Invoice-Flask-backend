from models import InvoiceModel
from db import db

def update_invoice(new_invoice, invoice_id):
    invoice_to_update=InvoiceModel.query.get(invoice_id)
    
    invoice_to_update.clientEmail=new_invoice["clientEmail"]
    invoice_to_update.clientName=new_invoice["clientName"]
    invoice_to_update.description=new_invoice["description"]
    invoice_to_update.paymentDue=new_invoice["paymentDue"]
    invoice_to_update.paymentTerms=new_invoice["paymentTerms"]
    invoice_to_update.status=new_invoice["status"]
    db.session.commit()
    