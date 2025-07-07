from rest_framework.viewsets import ModelViewSet
from app.models import Seller,ProductCategory,Product
from app.serializers import SellerSerializer,ProductCategorySerializer,ProductSerializer
class SellerViewSet(ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
class ProductCategoryViewSet(ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer