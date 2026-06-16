from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer

class ProductList(APIView):
    def get(self, request):
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.items.count() > 0:
            return Response(
                {'error': 'Product cannot be deleted because it is associated with an order item.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(APIView):
    def get(self, request):
        queryset = Collection.objects.select_related('featured_product').all()
        serializer = CollectionSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CollectionDetail(APIView):
    def get(self, request, id):
        collection = get_object_or_404(Collection, pk=id)
        serializer = CollectionSerializer(collection, context={'request': request})
        return Response(serializer.data)

    def put(self, request, id):
        collection = get_object_or_404(Collection, pk=id)
        serializer = CollectionSerializer(collection, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        collection = get_object_or_404(Collection, pk=id)
        if collection.product_set.count() > 0:
            return Response(
                {'error': 'Collection cannot be deleted because it has associated products.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)