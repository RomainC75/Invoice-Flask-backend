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

def big_update(received_items_list, oldItems, invoice_id):
    for oldItem in list(oldItems):
            if oldItem.id not in [ newItem['id'] for newItem in received_items_list if 'id' in newItem.keys() ]  :
                remove_item(oldItem.id)
    for i, newItem in enumerate(received_items_list):
        if( 'id' not in newItem.keys()):
            add_new_item(newItem,invoice_id)
    received_items_list = list( filter( lambda item : 'id' in item , received_items_list ) ) 
    for item in received_items_list:
        update_item(item)