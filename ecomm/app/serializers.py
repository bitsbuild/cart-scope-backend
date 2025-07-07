from rest_framework.serializers import ModelSerializer
from app.models import Seller,ProductCategory,Product
class SellerSerializer(ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'
class ProductCategorySerializer(ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'
class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'