from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product =  models.ForeignKey('Product', on_delete = models.SET_NULL, null=True, related_name='+')   #It tells Django not to apply the reverse relationship with product


    def __str__(self):
        return self.title


    class Meta:
        ordering = ['title']
    



# Promotion <===>  Product 
class Promotion(models.Model):
    description =  models.CharField(max_length=255)
    discount = models.FloatField()


class Product(models.Model):
    # sku =  models.CharField(max_length=10, primary_key=True)  if we dont have ID key
    title =  models.CharField(max_length=255)
    description = models.TextField(blank=True)    
    unit_price =  models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])
    slug =  models.SlugField()   # to make it easier for the search engine to find our products
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete = models.PROTECT)
    promotions =  models.ManyToManyField(Promotion, blank= True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']    

class Customer(models.Model):

    Member_Bronze = 'B'
    Member_Silver = 'S' 
    Member_Gold = 'G'
    MemberShip_Choices = [
        (Member_Bronze, 'Bronze'), 
        (Member_Silver, 'Silver'),
        (Member_Gold, 'Gold')
    ]
    first_name = models.CharField(max_length=255)
    last_name =  models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null= True)  # this filed is nullable

    membership =  models.CharField(max_length=1, choices=MemberShip_Choices, default= Member_Bronze)

   
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    

    class Meta:
        ordering = ['first_name', 'last_name']
        db_table = 'store_customer'
        indexes = [
            models.Index(fields=['last_name', 'first_name'])  # we used them just to speed up our query 
        ]


class Order(models.Model):
    Order_Pending =  'P'
    Order_Complete = 'C'
    Order_Failed = 'F'

    Order_Choices = [
        (Order_Pending, 'Pending'),
        (Order_Complete, 'Complete'),
        (Order_Failed, 'Failed')
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status =  models.CharField(max_length=1, choices=Order_Choices, default= Order_Pending)
    customer =  models.ForeignKey(Customer, on_delete = models.PROTECT)   ## models.Protects since in case we deleted the customer, we will not delete his orders from the database 
    
   

class OrderItem(models.Model):
    order =  models.ForeignKey(Order, on_delete = models.PROTECT)
    product = models.ForeignKey(Product, on_delete = models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price =  models.DecimalField(max_digits=6, decimal_places=2)



class Address(models.Model):
    street =  models.CharField(max_length=255)
    city =  models.CharField(max_length=255)
    # customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)  # primary key to let same customer has the same  address
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # same customer can have multiple addresses OnetoMany relation

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart =  models.ForeignKey(Cart, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveSmallIntegerField()