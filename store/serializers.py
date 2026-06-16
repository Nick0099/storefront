from decimal import Decimal
from store.models import Product, Collection
from rest_framework import serializers

class CollectionSerializer(serializers.ModelSerializer):
   products_count = serializers.IntegerField(read_only = True)
   class Meta:
        model = Collection
        fields= ['id', 'title', 'products_count']

   
class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField(method_name= 'calculate_tax')
    class Meta:
        model = Product
        fields = [ 'id', 'title', 'slug','inventory', 'description','price', 'price_with_tax', 'collection' ]

    

    def calculate_tax(self, product:Product):
        return product.price * Decimal(1.1)