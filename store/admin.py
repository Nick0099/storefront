from django.contrib import admin
from . import models

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
  list_display = ['title', 'price', 'inventory_status', 'collection_title']
  list_editable = ['price']
  list_per_page = 10
  list_select_related = ['collection']
  @admin.display(ordering = 'inventory')
  def inventory_status(self,product):
    if product.inventory < 10:
        return 'low'
    return 'OK'
  def collection_title(self, product):
     return product.collection.title
     

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
  list_display = ['id','customer',  'payment_status','placed_at']
  list_per_page = 10
 
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
  list_display = ['first_name', 'last_name', 'membership']
  list_editable = ['membership']
  ordering = ['first_name', 'last_name']
  list_per_page = 10

admin.site.register(models.Collection)