from django.db import models

# Create your models here.

class Promotion(models.Model):
    description = models.CharField(max_length = 255)
    discount = models.FloatField()
    
     

class Collection(models.Model):
    title = models.CharField(max_length = 255)
    featured_product = models.ForeignKey('Product', on_delete = models.SET_NULL, null = True, related_name = '+') 
    def __str__(self) -> str  :
        return self.title
    class Meta:
        ordering = ['title']

class Product(models.Model): 
    title = models.CharField(max_length = 255)
    slug = models.SlugField(null = True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete = models.PROTECT)
    promotions = models.ManyToManyField(Promotion) 
    def __str__(self) -> str:
        return self.title
    class Meta:
        ordering = ['title']

class Customer(models.Model):
    MEMBERSHIP_NONE = 'N'
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICE = [
        (MEMBERSHIP_NONE, 'None'),
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255, unique = True)
    phone = models.CharField(max_length = 255)
    birth_date = models.DateField(null = True)
    membership = models.CharField(max_length = 1, choices = MEMBERSHIP_CHOICE, default = 'N')
    def __str__(self):
       return f'{self.first_name} {self.last_name}'
    class Meta:
        ordering = ['first_name','last_name']
    class Meta:
        db_table = 'store_customers'
        indexes = [
            models.Index(fields = ['last_name' , 'first_name'] ),
        ]
    


class Order(models.Model):
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETE = 'C'  
    PAYMENT_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_PENDING, 'Pending'),
        (PAYMENT_COMPLETE, 'Complete'),
        (PAYMENT_FAILED, 'Failed'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length = 1, choices = PAYMENT_STATUS_CHOICES, default = 'P')
    customer = models.ForeignKey(Customer, on_delete = models.PROTECT)
   

class OrdersItem(models.Model):
    order = models.ForeignKey(Order, on_delete = models.PROTECT, related_name = 'items')
    product = models.ForeignKey(Product, on_delete = models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    
class Address(models.Model):
    street = models.CharField(max_length = 255)
    city = models.CharField(max_length = 255)
    zip = models.CharField(max_length = 10, null = True)
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
