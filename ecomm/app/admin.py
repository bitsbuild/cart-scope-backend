from django.contrib import admin
from app.models import Seller,ProductCategory,Product,ProductImages,Review,Order,CouponCode,OrderItem
admin.site.register(Seller)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(ProductImages)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(CouponCode)
admin.site.register(OrderItem)