# from email.policy import default
from django.db import models
import uuid
# from django.contrib.auth.models import User
from  django.conf import settings
# from UserProfile.models import Customer

# Create your models here.

        
class Category(models.Model):
    title = models.CharField(max_length=200)
    category_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    slug = models.SlugField(default= None)
    

    def __str__(self):
        return self.title
    

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    discount = models. BooleanField(default=False)
    image = models.ImageField(upload_to = 'img',  blank = True, null=True, default='')
    old_price = models.FloatField(default=100.00)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    slug = models.SlugField(default=None)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    inventory = models.IntegerField(default=5)
    top_deal=models.BooleanField(default=False)
    flash_sales = models.BooleanField(default=False)
    

    @property
    def price(self):
        if self.discount:
            new_price = self.old_price - ((30/100)*self.old_price)
        else:
            new_price = self.old_price
        return new_price
    
    @property
    def img(self):
        if self.image == "":
            self.image = ""
        
        return self.image

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True,related_name="images")
    image = models.ImageField(upload_to='media',blank=True,null=True,default='')
    
class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False,primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def _str__(self):
        return str(self.id)
    
class Cartitems(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,blank=True,null=True,related_name="carts")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True , null=True,related_name="cartitems")
    quantity = models.IntegerField(default=0)

class Profile(models.Model):
    pname = models.CharField(max_length=50)
    bio = models.TextField()
    img = models.ImageField(upload_to='media', blank=True , null=True)


class Order(models.Model):
    
    
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    pending_status = models.CharField(
        max_length=50, choices=PAYMENT_STATUS_CHOICES, default='PAYMENT_STATUS_PENDING')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.pending_status



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name = "orders_items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    

    def __str__(self):
        return self.product.name


# class Cart(models.Model):
#     owner = models.ForeignKey(Customer, on_delete=models.CASCADE, null = True, blank=True)
#     cart_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
#     created = models.DateTimeField(auto_now_add=True)
#     completed = models.BooleanField(default=False)
#     session_id = models.CharField(max_length=100)
    

#     @property
#     def num_of_items(self):
#         cartitems = self.cartitems_set.all()
#         qtysum = sum([ qty.quantity for qty in cartitems])
#         return qtysum
    
#     @property
#     def cart_total(self):
#         cartitems = self.cartitems_set.all()
#         qtysum = sum([ qty.subTotal for qty in cartitems])
#         return qtysum

#     def __str__(self):
#         return str(self.cart_id)

# class Cartitems(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, related_name='cartitems')
#     quantity = models.IntegerField(default=0)
    
    
#     @property
#     def subTotal(self):
#         total = self.quantity * self.product.price
        
#         return total
    
   

# class SavedItem(models.Model):
#     owner = models.ForeignKey(Customer, on_delete=models.CASCADE, null = True, blank=True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
#     added = models.IntegerField(default=0)
    
    
    
#     def __str__(self):
#         return str(self.id)
    