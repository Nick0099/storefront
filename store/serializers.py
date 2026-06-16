from decimal import Decimal
from store.models import Product, Collection
from rest_framework import serializers

class CollectionSerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField(method_name = 'get_product_count')
    class Meta:
        model = Collection
        fields= ['id', 'title', 'product_count']
    
    def get_product_count(self, collection:Collection):
        return Product.objects.filter(collection = collection).count()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [ 'id', 'title', 'slug','inventory', 'description','price', 'price_with_tax', 'collection' ]

    price_with_tax = serializers.SerializerMethodField(method_name= 'calculate_tax')
    

    def calculate_tax(self, product:Product):
        return product.price * Decimal(1.1)