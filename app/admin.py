from django.contrib import admin
from app.models import Customer,Product,Cart,OrderPlaced
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
  list_display=['user','name','locality','city','zipcode','state']
admin.site.register(Customer,CustomerAdmin)

class ProductAdmin(admin.ModelAdmin):
  list_display=['id','title','selling_price','discount_price','describtion','brand','catagory','product_img']
admin.site.register(Product,ProductAdmin)

class CartAdmin(admin.ModelAdmin):
  list_display=['id','user','product','quantity']
admin.site.register(Cart,CartAdmin)

class OrderPlacedAdmin(admin.ModelAdmin):
  list_display=['id','user','customer','product','quantity','order_date','status']
admin.site.register(OrderPlaced,OrderPlacedAdmin)  