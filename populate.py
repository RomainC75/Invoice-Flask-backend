import json
import datetime
import sqlite3
con = sqlite3.connect("instance/data.db")
cur = con.cursor()

res = cur.execute("SELECT * FROM invoices")
print("====> res, ",res.fetchall())

def add_invoice(data,current_user_id, senderAddress_id, clientAddress_id):
    cur.execute("""
        INSERT 
        INTO `invoices` (`createdAt`,`paymentDue`, `description`, `clientName`, `clientEmail`, `status`, `paymentTerms`, `senderAddress_id`, `clientAddress_id`, `user_id`)
        VALUES (?,?,?,?,?,?,?,?,?,?)
    """, (data['createdAt']+' 00:00:00.000000', data["paymentDue"]+' 00:00:00.000000', data["description"], data["clientName"], data["clientEmail"], data["status"], data['paymentTerms'], senderAddress_id, clientAddress_id, current_user_id) )
    con.commit()


def add_clientAddress(address_data:dict,name:str):
    cur.execute("""
        INSERT 
        INTO `clientAddresses` (`name`,`street`,`city`,`postCode`,`country`) 
        VALUES (?,?,?,?,?)
    """, (name, address_data['street'], address_data['city'], address_data['postCode'], address_data['country']) )
    con.commit()

def add_senderAddress(address_data:dict,name:str):
    cur.execute("""
        INSERT 
        INTO `senderAddresses` (`name`,`street`,`city`,`postCode`,`country`) 
        VALUES (?,?,?,?,?)
    """, (name, address_data['street'], address_data['city'], address_data['postCode'], address_data['country']) )
    con.commit()

def add_item(item, invoice_id):
    cur.execute("""
        INSERT
        INTO `items` (`name`,`quantity`,`price`,`invoice_id`)
        VALUES (?,?,?,?)
    """, (item['name'], item['quantity'], item['price'], invoice_id))
    con.commit()

with open("populate/data.json", "r") as data_file:
    invoices = json.load(data_file)
    for invoice in invoices:
        print("==",invoice)

        add_senderAddress(invoice['senderAddress'], invoice['clientName'])
        senderAddress_id=cur.lastrowid
        print('senderAddress_id : ', senderAddress_id)
        
        add_clientAddress(invoice['clientAddress'], invoice['clientName'])
        clientAddress_id=cur.lastrowid
        print('clientAddress_id', clientAddress_id)
        
        add_invoice(invoice, 1, 1, 1)
        invoice_id=cur.lastrowid
        print("invoice_id : ",clientAddress_id)
        
        for item in invoice['items']:
            add_item(item,invoice_id)


