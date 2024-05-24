from django.shortcuts import render
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
# from rest_framework.response import Response
from  storeapp.models import Product, Category,Cart,Cartitems,Profile,Order,OrderItem
from .serializer import productserializer,categoryserializer,cartserializer,cartitemsSerializer,AddCartItemSerializer,UpdateCartItemSerializer,ProfileSerializer,OrderitemSerializer,OrderSerializer,OrderCreateSerializer
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from api.filter import ProductFilter #this is customise filter
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,ListModelMixin,DestroyModelMixin
from rest_framework.permissions import IsAuthenticated

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = productserializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = ProductFilter #customize filter
    search_fields = ['name','description'] #impliment search filter for searching
    ordering_fields = ['old_price']  # impliment ordering filter for ascending and desecending order
    pagination_class = PageNumberPagination # this class use for page number 

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = categoryserializer

class CartViewSet(CreateModelMixin,ListModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = cartserializer

class CartItemViewSet(ModelViewSet):
    http_method_names = ['get','post','patch','delete']
    # queryset = Cartitems.objects.all()
    def get_queryset(self):
        return Cartitems.objects.filter(cart_id=self.kwargs["cart_nest_pk"])
    # serializer_class = cartitemsSerializer
    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        if self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return cartitemsSerializer
    
    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_nest_pk"]}
    
class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    # queryset =  Order.objects.all()
    # serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
             return OrderCreateSerializer
        return OrderSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(owner =user)  
    
    def get_serializer_context(self):
        return {"user_id":self.request.user.id}
     
# class ApiProduct(APIView):
#     def get(self,request,pk=None,format=None):
#         if pk is None:
#             data = Product.objects.all()
#             seri_data = productserializer(data, many = True)
#             return Response(seri_data.data)
#         else:
#             data = Product.objects.get(id=pk)
#             seri_data = productserializer(data)
#             return Response(seri_data.data)
        
#     def post(self, request,pk=None,format=None):
#         product_seri = productserializer(data=request.data)
#         if product_seri.is_valid():
#             product_seri.save()
#             return Response({'msg':'successfully Insert data'})
#         else:
#              return Response(product_seri.errors)
        
#     def put(self,request,pk=None,format=None):
#         if pk is not None:
#             old_data = Product.objects.get(id=pk)
#             product_seri = productserializer(old_data, data=request.data)
#             if product_seri.is_valid():
#                 product_seri.save()
#                 return Response({'msg':'update data successfully'})
#         else:
#              return Response(product_seri.errors)
        
#     def delete(self,request,pk=None,format=None):
#         if pk is not None:
#             fetch_data = Product.objects.get(id = pk)
#             fetch_data.delete()
#             return Response({'msg':'data delete successfully'})


# class ApiCategory(APIView):
#     def get(self,request,pk=None,format=None):
#         if pk is None:
#             data = Category.objects.all()
#             seri_data = categoryserializer(data, many = True)
#             return Response(seri_data.data)
#         else:
#             data = Category.objects.get(category_id=pk)
#             seri_data = categoryserializer(data)
#             return Response(seri_data.data)
        
#     def post(self,request,pk=None,format=None):
#         cat_seri = categoryserializer(data=request.data)
#         if cat_seri.is_valid():
#             cat_seri.save()
#             return Response({'msg':'successfully Insert data'})
#         else:
#              return Response(cat_seri.errors)
        
#     def put(self,request,pk=None,format=None):
#         if pk is not None:
#             old_data = Category.objects.get(category_id=pk)
#             cat_seri = categoryserializer(old_data, data=request.data)
#             if cat_seri.is_valid():
#                 cat_seri.save()
#                 return Response({'msg':'successfully Insert data'})
#         else:
#              return Response(cat_seri.errors)
        
#     def delete(self,request,pk=None,format=None):
#         if pk is not None:
#             fetch_data = Category.objects.get(category_id = pk)
#             fetch_data.delete()
#             return Response({'msg':'data delete successfully'})

# Create your views here.
