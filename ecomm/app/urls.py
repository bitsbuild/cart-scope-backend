from rest_framework.routers import DefaultRouter
from app.views import SellerViewSet,ProductCategoryViewSet,ProductViewSet,ProductImagesViewSet
router = DefaultRouter()
router.register(r'seller',SellerViewSet,basename='seller')
router.register(r'category',ProductCategoryViewSet,basename='category')
router.register(r'product',ProductViewSet,basename='product')
router.register(r'productimages',ProductImagesViewSet,basename='productimages')
urlpatterns = router.urls
