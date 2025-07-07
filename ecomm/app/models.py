from django.db.models import (
    Model,
    UUIDField,
    CharField,
    TextField,
    DateTimeField,
    ForeignKey,
    IntegerField,
    BigIntegerField,
    FloatField,
    BooleanField,
    CASCADE,
)
from django.core.validators import MinValueValidator,MaxValueValidator
import uuid
class ProductCategory(Model):
    id = UUIDField(primary_key=True,editable=False,default=uuid.uuid4,blank=False)
    name = CharField(max_length=700,blank=False)
    def __str__(self):
        return self.name
class Seller(Model):
    id = UUIDField(primary_key=True,default=uuid.uuid4,editable=False,blank=False)
    name = CharField(max_length=700,blank=False)
    about = TextField(max_length=3500,blank=False)
    postal_code = BigIntegerField(blank=False)
    location = TextField(blank=False)
    is_premium_seller = BooleanField(default=False,blank=False,editable=False)
    rating = FloatField(validators=[MinValueValidator(0),MaxValueValidator(5)],default=0,blank=False,editable=False)
    created = DateTimeField(auto_now_add=True,editable=False,blank=False)
    updated = DateTimeField(auto_now=True,editable=False,blank=False)
    def __str__(self):
        return self.name
class Product(Model):
    id = UUIDField(primary_key=True,editable=False,default=uuid.uuid4,blank=False)
    name = CharField(max_length=700,blank=False)
    about = TextField(max_length=3500,blank=False)
    category = ForeignKey(ProductCategory,related_name='products',on_delete=CASCADE,blank=False)
    seller = ForeignKey(Seller,related_name='inventory',on_delete=CASCADE,blank=False)
    quantity = IntegerField(blank=False)
    price = IntegerField(blank=False)
    rating = FloatField(validators=[MinValueValidator(0),MaxValueValidator(5)],default=0,blank=False,editable=False)
    created = DateTimeField(auto_now_add=True,editable=False,blank=False)
    updated = DateTimeField(auto_now=True,editable=False,blank=False)
    def __str__(self):
        return self.name