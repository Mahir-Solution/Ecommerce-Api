from django.contrib import admin
from .models import Category,Product,Cart,Cartitems,ProductImage,Profile,Order,OrderItem
@admin.register(Category)
class categoryadmin(admin.ModelAdmin):
    list_display = ['title','category_id','slug']
    prepopulated_fields = {'slug':('title',)}

@admin.register(Product)
class productadmin(admin.ModelAdmin):
    list_display = ['id','name','description','discount','image','old_price','category','slug','inventory']
    prepopulated_fields = {'slug':('name',)}
# Register your models here.

@admin.register(Cart)
class cartadmin(admin.ModelAdmin):
    list_display = ['id','created_date']

@admin.register(Cartitems)
class cartitemsadmin(admin.ModelAdmin):
    list_display = ['id','cart','product','quantity']

@admin.register(ProductImage)
class productimageadmin(admin.ModelAdmin):
    list_display = ['id','product','image']

@admin.register(Profile)
class profileadmin(admin.ModelAdmin):
    list_display = ['id','pname','bio','img']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','placed_at','pending_status','owner']
    
@admin.register(OrderItem)
class profileadmin(admin.ModelAdmin):
    list_display = ['id','order','product','quantity']

