from rest_framework.viewsets import ModelViewSet
from app.models import Seller,ProductCategory,Product,ProductImages,Review,Order,CouponCode,OrderItem
from app.serializers import SellerSerializer,ProductCategorySerializer,ProductSerializer,ProductImagesSerializer,ReviewSerializer,OrderSerializer,CouponCodeSerializer,OrderItemSerializer
import statistics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from django.contrib.auth.models import User
import weasyprint
from django.core.files.base import ContentFile
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
        customer = User.objects.get(pk=request.data['customer'])
        coupon_code = CouponCode.objects.get(name=request.data['coupon_code'])
        order = Order.objects.create(
            customer=customer,
            coupon_code=coupon_code
        )
        order_items = []
        details_for_bill = []
        for i in request.data['order_items']:
            prod = Product.objects.get(pk=i['product'])
            quant = int(i['quantity'])
            pro_price = prod.price
            amnt = pro_price*quant
            order_items.append(OrderItem.objects.create(
                                      order=order,
                                      product=prod,
                                      quantity=quant,
                                      product_price=pro_price,
                                      amount = amnt
                                    ))
            details_for_bill.append([
                order,prod,quant,pro_price,amnt
            ])
        amount = 0
        for i in details_for_bill:
            amount = amount + i[4]
        order.amount = amount
        order.discount = ((int(CouponCode.objects.get(name=request.data['coupon_code']).discount_percentage)*amount)/100) if CouponCode.objects.get(name=request.data['coupon_code']) else 0
        order.final_amount = order.amount - order.discount
        html_string = ''
        order.invoice.save(f'{order.id}.pdf',ContentFile(weasyprint.HTML(string=html_string).write_pdf()),save=False)
        order.save()
        try:
            return Response(
                {
                    'Status':'Ordered Place Successfully!'
                },status=HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'Status':'So Sorry, Order Could Not Be Placed!',
                    'Error':str(e)
                },status=HTTP_400_BAD_REQUEST
            )
class CouponCodeViewSet(ModelViewSet):
    queryset = CouponCode.objects.all()
    serializer_class = CouponCodeSerializer
class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer