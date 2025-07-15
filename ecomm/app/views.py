from rest_framework.viewsets import ModelViewSet
from app.models import Seller,ProductCategory,Product,ProductImages,Review,Order,CouponCode,OrderItem
from app.serializers import SellerSerializer,ProductCategorySerializer,ProductSerializer,ProductImagesSerializer,ReviewSerializer,OrderSerializer,CouponCodeSerializer,OrderItemSerializer
import statistics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from django.contrib.auth.models import User
import weasyprint
from django.core.files.base import ContentFile
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
from django.db import transaction
from rest_framework.permissions import IsAdminUser,IsAuthenticated
import app.permissions as rp
class SellerViewSet(ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ['postal_code','created','updated','rating','location','is_premium_seller']
    search_fields = ['id','name','postal_code','created','updated','rating','location','is_premium_seller']
    ordering_fields = ['id','name','postal_code','created','updated','rating','location','is_premium_seller']
class ProductCategoryViewSet(ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAdminUser]
    search_fields = ['id','name']
    ordering_fields = ['id','name']
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ['category','seller','price','rating','created','updated']
    search_fields = ['id','name','category','seller','price','rating','created','updated']
    ordering_fields = ['id','name','category','seller','price','rating','created','updated']
class ProductImagesViewSet(ModelViewSet):
    queryset=ProductImages.objects.all()
    serializer_class=ProductImagesSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ['product']
    search_fields = ['id','product']
    ordering_fields = ['product','id']
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated,rp.ReviewPermissions]
    filterset_fields = ['user','product','stars','created','updated']
    search_fields = ['id','user','product','stars','created','updated','title']
    ordering_fields = ['id','user','product','stars','created','updated','title']
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
    permission_classes = [IsAuthenticated,rp.OrderPermissions]
    http_method_names = ['post','get']
    search_fields = ['id','customer','created','updated']
    ordering_fields = ['id','customer','created','updated']
    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
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
                html_string = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Invoice #{order.id}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 40px;
                }}
                .invoice-box {{
                    max-width: 800px;
                    margin: auto;
                    padding: 30px;
                    border: 1px solid #eee;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.15);
                    line-height: 24px;
                    font-size: 16px;
                    color: #555;
                }}
                .invoice-box table {{
                    width: 100%;
                    line-height: inherit;
                    text-align: left;
                }}
                .invoice-box table td {{
                    padding: 5px;
                    vertical-align: top;
                }}
                .invoice-box table tr.heading td {{
                    background: #eee;
                    border-bottom: 1px solid #ddd;
                    font-weight: bold;
                }}
                .invoice-box table tr.item td {{
                    border-bottom: 1px solid #eee;
                }}
                .invoice-box table tr.total td:nth-child(5) {{
                    border-top: 2px solid #eee;
                    font-weight: bold;
                }}
                h2 {{
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    font-size: 12px;
                    color: #999;
                }}
            </style>
        </head>
        <body>
            <div class="invoice-box">
                <h2>Order Invoice</h2>
                <table cellpadding="0" cellspacing="0">
                    <tr class="heading">
                        <td>Order ID:</td>
                        <td>{order.id}</td>
                        <td>Customer ID:</td>
                        <td>{customer.id}</td>
                    </tr>
                    <tr class="heading">
                        <td>Email:</td>
                        <td colspan="3">{customer.email}</td>
                    </tr>
                </table>

                <br>

                <table cellpadding="0" cellspacing="0">
                    <tr class="heading">
                        <td>Product</td>
                        <td>Quantity</td>
                        <td>Unit Price</td>
                        <td>Line Total</td>
                    </tr>

                    {''.join(f"""
                    <tr class="item">
                        <td>{i[1].name}</td>
                        <td>{i[2]}</td>
                        <td>₹{i[3]}</td>
                        <td>₹{i[4]}</td>
                    </tr>
                    """ for i in details_for_bill)}

                    <tr class="total">
                        <td></td>
                        <td></td>
                        <td>Subtotal:</td>
                        <td>₹{order.amount}</td>
                    </tr>
                    <tr class="total">
                        <td></td>
                        <td></td>
                        <td>Discount:</td>
                        <td>- ₹{order.discount}</td>
                    </tr>
                    <tr class="total">
                        <td></td>
                        <td></td>
                        <td>Total:</td>
                        <td>₹{order.final_amount}</td>
                    </tr>
                </table>

                <div class="footer">
                    Thank you for shopping with us!<br>
                    This is a system generated invoice.
                </div>
            </div>
        </body>
        </html>
        """
                file_name = f'{order.id}.pdf'
                order.invoice.save(file_name,ContentFile(weasyprint.HTML(string=html_string).write_pdf()),save=False)
                order.save()
                load_dotenv()
                msg = EmailMessage()
                msg['Subject'] = 'Your Order Was Placed Successfully'
                msg['From'] = os.getenv('EMAIL_USER')
                msg['To'] = str(customer.email)
                msg.set_content('Find Attached Invoice For Your Order, Keep Shopping!!!')
                with order.invoice.open('rb') as f:
                    file_data = f.read()
                msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)
                with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                    smtp.starttls()
                    smtp.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))
                    smtp.send_message(msg)
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
    permission_classes = [IsAdminUser]
    filterset_fields = ['discount_percentage']
    search_fields = ['name','code','discount_percentage']
    ordering_fields = ['name','code','discount_percentage']
class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAdminUser]
    search_fields = ['id']