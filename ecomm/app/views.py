from rest_framework.viewsets import ModelViewSet
from app.models import Seller,ProductCategory,Product,ProductImages,Review,Order,CouponCode,OrderItem
from app.serializers import SellerSerializer,ProductCategorySerializer,ProductSerializer,ProductImagesSerializer,ReviewSerializer,OrderSerializer,CouponCodeSerializer,OrderItemSerializer
import statistics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
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
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            product = request.data['product']
            reviews = list(Review.objects.filter(product=product).values_list('stars',flat=True))
            rating_product = statistics.mean(reviews)
            product_review_change = Product.objects.get(pk=product)
            product_review_change.rating = rating_product
            product_review_change.save()
            return Response(
                {
                "Status":"Successfully Added The Review And The Rating (stars) Reflects In Prodct Rating",
                },
                status=HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "Status":"Failure To Create Review",
                    "Error":str(e)
                },
                status=HTTP_400_BAD_REQUEST
            )
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    def create(self, request, *args, **kwargs):
        try:
            order = Order.objects.create()
            return Response(
                {
                    "Status":"Order Placed Successfully"
                },
                status=HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "Status":"Order Placement Failure",
                    "Error":str(e)
                },
                status=HTTP_400_BAD_REQUEST
            )
class CouponCodeViewSet(ModelViewSet):
    queryset = CouponCode.objects.all()
    serializer_class = CouponCodeSerializer
class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer