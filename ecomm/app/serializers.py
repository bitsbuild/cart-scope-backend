from rest_framework.serializers import ModelSerializer,BooleanField,PrimaryKeyRelatedField,SlugRelatedField
from app.models import Seller,ProductCategory,Product,ProductImages,Review,Order
class ReviewSerializer(ModelSerializer):
    product = PrimaryKeyRelatedField(queryset=Product.objects.all())
    class Meta:
        model = Review
        fields = '__all__'
class ProductImagesSerializer(ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'
class ProductSerializer(ModelSerializer):
    images = ProductImagesSerializer(many=True,read_only=True)
    reviews = ReviewSerializer(many=True,read_only=True)
    class Meta:
        model = Product
        fields = '__all__'
class SellerSerializer(ModelSerializer):
    is_premium_seller = BooleanField(read_only=True)
    inventory = ProductSerializer(many=True,read_only=True)
    class Meta:
        model = Seller
        fields = '__all__'
class ProductCategorySerializer(ModelSerializer):
    products = ProductSerializer(many=True,read_only=True)
    class Meta:
        model = ProductCategory
        fields = '__all__'
class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
    