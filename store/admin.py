from itertools import count
from django.db.models import Count
from django.contrib import admin, messages
from django.utils.html import format_html , urlencode
from django.urls import reverse
from . import models


class InventoryFilter(admin.SimpleListFilter):
   title = 'inventory'
   parameter_name = ' inventory'

   def lookups(self, request, model_admin):
      return [
         ('<10', 'low')
      ]
   def queryset(self,request, queryset):
      if self.value() == '<10':
         return queryset.filter(inventory__lt = 10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
  autocomplete_fields = ['collection']
  search_fields= ['title']
  prepopulated_fields = {
     'slug' : ['title']

  }
  actions = ['clear_inventory']
  list_display = ['title', 'price', 'inventory_status', 'collection_title']
  list_editable = ['price']
  list_per_page = 10
  list_select_related = ['collection']
  list_filter  =  ['collection', 'last_update', InventoryFilter]
 
  @admin.display(ordering = 'inventory')
 
  def inventory_status(self,product):
    if product.inventory < 10:
        return 'low'
    return 'OK'
 
  def collection_title(self, product):
     return product.collection.title
 
  @admin.action(description='Clear inventory')
 
  def clear_inventory(self, request,queryset):
     updated_count = queryset.update(inventory = 0)
     self.message_user(
        request, f'{updated_count} products were successfully updated',
        messages.SUCCESS
     )

class OrderItemInline(admin.TabularInline):
   autocomplete_fields = ['product']
   model = models.OrdersItem  
   extra = 0   
   min_num = 1
   max_num = 10

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
  list_display = ['id','customer',  'payment_status','placed_at']
  inlines = [OrderItemInline]
  list_per_page = 10  
  autocomplete_fields = ['customer']


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'order_count']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    search_fields = ['^first_name', '^last_name']

    @admin.display(ordering='order_count')
    def order_count(self, customer):
        url = (reverse('admin:store_order_changelist') + '?' + urlencode({'customer_id': str(customer.id)}))
        return format_html('<a href="{}">{}</a>', url, customer.order_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            order_count=Count('order')
        )

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']
    @admin.display(ordering='products_count')
    def products_count(self,collection):
       url = (reverse('admin:store_product_changelist')
       + '?' + urlencode({
          'collection_id': str(collection.id)
       }))
       return format_html('<a href="{url}">{count}</a>', url=url, count=collection.products_count)
    
    def get_queryset(self,request):
       return super().get_queryset(request).annotate(
          products_count= Count('product')
       )
    