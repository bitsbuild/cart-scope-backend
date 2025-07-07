from rest_framework.serializers import ModelSerializer,BooleanField
from app.models import Seller,ProductCategory,Product
class SellerSerializer(ModelSerializer):
    is_premium_seller = BooleanField(read_only=True)
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