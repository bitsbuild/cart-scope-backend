from django.db import models
import uuid
class ProductCategory(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.name
# Product Category Model Development Complete
class Seller(models.Model):
    pass
class Product(models.Model):
    pass
class ProductReview(models.Model):
    pass
class Cart(models.Model):
    pass
class Order(models.Model):
    pass
