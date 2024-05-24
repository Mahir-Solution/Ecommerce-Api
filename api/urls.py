from django.urls import path,include
# from .views import ApiProduct,ApiCategory
from . import  views
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router = DefaultRouter()
router.register("product",views.ProductViewSet)
router.register("category",views.CategoryViewSet)
router.register("cart",views.CartViewSet)
router.register("profile",views.ProfileViewSet)
router.register("order",views.OrderViewSet,basename="order")
# routers.NestedDefaultRouter()
cart_router = routers.NestedDefaultRouter(router, "cart", lookup="cart_nest")
cart_router.register("items",views.CartItemViewSet, basename="cart_items")


urlpatterns = router.urls
urlpatterns = [
    path("",include(router.urls)),
    path("",include(cart_router.urls)),
    # path('product/',ApiProduct.as_view()),
    # path('product/<str:pk>/',ApiProduct.as_view()),
    # path('category/',ApiCategory.as_view()),
    # path('category/<str:pk>/',ApiCategory.as_view()),
]
