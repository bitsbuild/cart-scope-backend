from rest_framework.viewsets import ModelViewSet
from app.models import Seller,ProductCategory,Product,ProductImages,Review,Order
from app.serializers import SellerSerializer,ProductCategorySerializer,ProductSerializer,ProductImagesSerializer,ReviewSerializer,OrderSerializer
class SellerViewSet(ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
class ProductCategoryViewSet(ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
class ProductImagesViewSet(ModelViewSet):
    queryset=ProductImages.objects.all()
    serializer_class=ProductImagesSerializer
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer