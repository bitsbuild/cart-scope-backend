from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator
class ProductCategory(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.name
# Product Category Model Development Complete
class Product(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=200)
    seller = models.ManyToManyField(related_name='products',)
class Seller(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=100,unique=True)
class ProductReview(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=1000)
    purchase_verification_status = models.BooleanField(default=False,editable=False)
    stars = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,editable=False)
    updated = models.DateTimeField(auto_now=True,editable=False)
    class Meta:
        unique_together = ('customer','product')
    def __str__(self):
        return self.title
# Product Review Model Development Complete
class Cart(models.Model):
    pass
class Order(models.Model):
    pass
