from django_filters.rest_framework import FilterSet
from storeapp.models import Product

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'category_id': ['exact'],
            'old_price': ['gt','lt']
        }
        

#this is customize filter 