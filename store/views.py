from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CartSerializer, ProductSerializer, CollectionSerializer,CartItemSerializer ,ReviewSerializer
from .models import Product, Collection, OrdersItem, Review, CartItem,Cart
from .fileter import ProductFilter
from .pagination import DefaultPagination
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']
    ordering_fields = [ 'price', 'last_update']

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrdersItem.objects.filter(product_id = kwargs['pk']).count() > 0:
            return Response(
                {'error': 'Product cannot be deleted because it is associated with an order item.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().destroy(request, *args, **kwargs)

class CollectionViewSet(ModelViewSet):
    queryset =   Collection.objects.annotate(products_count = Count('product')).all()
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
        return {'request': self.request}
    def destroy(self, request, *args, **kwargs):
         collection = get_object_or_404(Collection, pk=kwargs['pk'])
         if collection.products_set.count > 0:
            return Response(
                {'error': 'Collection cannot be deleted because it has associated products.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
         return super().destroy(request, *args, **kwargs)
    
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    
class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    
    def get_queryset(self):
        return Cart.objects.all()
    
class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])
    