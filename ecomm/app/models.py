from django.db import models
import uuid
class Product(models.Model):
    id = models.UUIDField(primary_key=True,read_only=True,default=uuid.uuid4)
    name = models.CharField()
    about = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)