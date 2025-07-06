from django.db.models import (
    Model,
    UUIDField,
    CharField,
    TextField,
    DateTimeField,
    ForeignKey,
    CASCADE,
    IntegerField,
    BigIntegerField
)
import uuid
class Seller(Model):
    id = UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = CharField()
    about = TextField()
    location = TextField()
    postal_code = BigIntegerField()
    created = DateTimeField(auto_now_add=True,editable=False)
    updated = DateTimeField(auto_now=True,editable=False)
class Product(Model):
    id = UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    name = CharField()
    about = TextField()
    amount = IntegerField()
    price = IntegerField()
    created = DateTimeField(auto_now_add=True,editable=False)
    updated = DateTimeField(auto_now=True,editable=False)
    seller = ForeignKey(Seller,related_name='inventory',on_delete=CASCADE)