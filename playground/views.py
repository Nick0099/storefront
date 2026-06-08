from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,F 
from django.http import HttpResponse
from store.models import Product, Order

def say_hello(request):
    try:  
      queryset = Order.objects.select_related('customer').order_by('-placed_at')[:5]
    except ObjectDoesNotExist:
         return HttpResponse('Product not found')

    return render(request, 'hello.html', {'name': 'Nischal', 'orders': queryset})