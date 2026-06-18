from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('cart', views.CartViewSet, basename = 'carts')


products_router = routers.NestedDefaultRouter(router, 'products',lookup = 'product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviws')

cart_router = routers.NestedDefaultRouter(router, 'cart',lookup = 'cart')
cart_router.register('item', views.CartItemViewSet, basename='cart-items')


urlpatterns = router.urls + products_router.urls + cart_router.urls