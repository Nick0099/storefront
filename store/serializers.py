from decimal import Decimal
from store.models import Product, Collection
from rest_framework import serializers

class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length = 255)
    

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length = 255 ) 
    price = serializers.DecimalField(max_digits= 5, decimal_places=2)
    price_with_tax = serializers.SerializerMethodField(method_name= 'calculate_tax')
    collection = serializers.HyperlinkedRelatedField(
        queryset = Collection.objects.all(),
        view_name = 'collection-detail',
    )


    def calculate_tax(self, product:Product):
        return product.price * Decimal(1.1)
    