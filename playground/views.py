from django.shortcuts import render
from store.models import Product, Order, OrdersItem,Customer,Collection

def say_hello(request):
      return render(request, 'hello.html', {'name': 'Nischal'})