
from marshmallow import Schema, fields, validate

class AddressSchema(Schema):
    id = fields.Integer(required=True, dump_only=True)
    # id = fields.Integer(required=True)
    name = fields.Str()
    street = fields.Str()
    city = fields.Str()
    postCode = fields.Str()
    country = fields.Str()

class ItemSchema(Schema):
    # id = fields.Integer(required=True, dump_only=True)
    id = fields.Integer()
    name= fields.Str(required=True)
    quantity= fields.Float(required=True)
    price= fields.Float()

class InvoiceSchema(Schema):
    id = fields.Integer(required=True, dump_only=True)
    user_id = fields.Int(dump_only=True)
    createdAt = fields.Date(format='%Y-%m-%d %H:%M:%S.%z')
    paymentDue = fields.Date(format='%Y-%m-%d')
    paymentTerms= fields.Int()
    description= fields.Str(required=True)
    clientName= fields.Str(required=True)
    clientEmail= fields.Str(required=True)
    status= fields.Str(validate=validate.OneOf(["paid","draft","pending"]))
    clientAddress = fields.Nested(AddressSchema)
    senderAddress = fields.Nested(AddressSchema)
    items = fields.List(fields.Nested(ItemSchema))

class UserSchema(Schema):
    id = fields.Integer(required=True,dump_only=True)
    email = fields.Str(required=True)
    username = fields.Str()
    password = fields.Str(required=True, load_only=True)
    avatar = fields.Url()