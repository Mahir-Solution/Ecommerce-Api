from rest_framework import serializers
from storeapp.models import Product,Category,Cart,Cartitems,ProductImage,Profile,Order,OrderItem


class categoryserializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_id", "title", "slug"]

class productimageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id','product','image']


class productserializer(serializers.ModelSerializer):
    images = productimageSerializer(many=True)
    uploaded_images = serializers.ListField(
                         child = serializers.ImageField(max_length=100000, allow_empty_file=False,use_url=False),
                        write_only=True
            )
    class Meta:
        model = Product
        
        fields = [ "id", "name", "description", "inventory", "price",'images','uploaded_images']

    def create(self,validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        prod = Product.objects.create(**validated_data)
        for img in uploaded_images:
            new_product = ProductImage.objects.create(proudct =prod,image = img)

        return prod


class simpleproductserializer(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields = ['id','name','price']


class cartitemsSerializer(serializers.ModelSerializer):
    product = simpleproductserializer(many=False)
    sub_total = serializers.SerializerMethodField(method_name="total")
    class Meta:
        model = Cartitems
        fields = ['id','cart','product','quantity','sub_total']

    def total(self,cartitem:Cartitems):
        return cartitem.quantity*cartitem.product.price


class cartserializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True)
    carts = cartitemsSerializer(many=True,read_only=True)# THIS IS NESTED SERILIZER and read only true mean it used for serilization and not for deserilization
    grand_total = serializers.SerializerMethodField(method_name="g_total")
    class Meta:
        model = Cart
        fields = ['id','created_date','carts','grand_total'] # here carts a related name filed that is used for reverse relations

    def g_total(self, cart:Cart):
        items = cart.carts.all()
        main_total = sum([x.quantity*x.product.price for x in items])
        return main_total
    
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField()
    
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("There is no product associated with the given ID")
        
        return value
    
    def save(self, **kwargs):
        cart_id = self.context.get("cart_id") # he is receive cart_id from view(get_serializer_context) as a key
        if cart_id is None:
            raise serializers.ValidationError("cart_nested_id is missing in context")
        product_id = self.validated_data["product_id"] 
        quantity = self.validated_data["quantity"] 
        
        try:
            cartitem = Cartitems.objects.get(product_id=product_id, cart_id=cart_id)
            cartitem.quantity += quantity
            cartitem.save()
            
            self.instance = cartitem
            
        
        except:
            
            self.instance = Cartitems.objects.create(cart_id=cart_id, **self.validated_data)
            
        return self.instance
    class Meta:
        model = Cartitems
        fields = ['id','product_id','quantity']

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cartitems
        fields = ['quantity']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id','pname','bio','img']

class OrderitemSerializer(serializers.ModelSerializer):
    product = simpleproductserializer()
    class Meta:
        model = OrderItem
        fields = ['order','product','quantity']

class OrderSerializer(serializers.ModelSerializer):
    orders_items = OrderitemSerializer(many=True, read_only = True)
    class Meta:
        model =  Order
        fields = ['id','placed_at','pending_status','owner','orders_items']

class OrderCreateSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def save(self, **kwargs):
        cart_id = self.validated_data["cart_id"]
        user_id = self.context["user_id"]
        order = Order.objects.create(owner_id=user_id)
        cartitems = Cartitems.objects.filter(cart_id=cart_id)
        orderitems = [
            OrderItem(
                order=order,
                product =item.product,
                quantity = item.quantity,
            )
            for item in cartitems
        ]
        OrderItem.objects.bulk_create(orderitems)
        Cart.objects.filter(id=cart_id).delete()


        return order
