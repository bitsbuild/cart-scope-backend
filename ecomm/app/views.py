from rest_framework.viewsets import ModelViewSet
from app.billing import billing
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
            order = Order.objects.create(customer=request.user.pk,coupon_code=request.data['coupon_code'])
            order_id = order.id
            order_items_id_list = []
            order_items_quantity_list = []
            order_items_price_list = []
            order_items_product_names = []
            for i in request.data['order_items']:
                quant = int(i['quantity'])
                order_items_quantity_list.append(quant)
                pro_price = int(Product.objects.get(pk=i['product']).price)
                order_items_price_list.append(pro_price)
                prod = i['product']
                product_name = Product.objects.get(pk=prod).name
                order_items_product_names.append(product_name)
                order_items_id_list.append(OrderItem.objects.create(
                    product=prod,
                    order=order_id,
                    quantity=quant,
                    product_price=pro_price,
                    amount=quant*pro_price,
                ).pk)
            try:
                disc = float(CouponCode.objects.get(name=request.data['coupon_code']).discount_percentage)
            except:
                disc = 0
            bill_response = billing(
                product_name_list=order_items_product_names,
                product_price_list=order_items_price_list,
                product_quantity_list=order_items_quantity_list,
                discount_percentage=disc
            )
            order.order_items = order_items_id_list
            order.amount = bill_response['amount']
            order.discount = bill_response['discount']
            order.final_amount = bill_response['final_amount']
            order.invoice = bill_response['invoice']
            order.save()
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