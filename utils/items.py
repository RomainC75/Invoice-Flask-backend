from db import db
from models import ItemModel

def add_new_item(item, invoice_id):
    new_item= ItemModel(**item, invoice_id=invoice_id)
    db.session.add(new_item)
    db.session.commit()

def update_item(item):
    item_to_update=ItemModel.query.get(item['id'])
    
    item_to_update.name=item["name"]
    item_to_update.price=item["price"]
    item_to_update.quantity=item["quantity"]
            
    db.session.commit()
    

def remove_item(item_id):
    print(f'==> {item_id} has to be removed ')
    item_to_delete=ItemModel.query.get(item_id)
    db.session.delete(item_to_delete)
    db.session.commit()