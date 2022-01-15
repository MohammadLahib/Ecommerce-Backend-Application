from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, OrderItem, Order, Customer, Collection
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.db.models.functions import Concat
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItem
from django.db import transaction

from django.db.models import Q, F, Func, Value, Count, ExpressionWrapper

# # Create your views here.
# # request -> response
# # request handler 
# #action
@transaction.atomic()
def say_hello(request):
#     # product = Product.objects.get()  # all method return a query set
#     # exists = Product.objects.filter(pk = 0).exists()
#     # queryset = Product.objects.filter(unit_price__range=(20, 30))
#     # queryset = Product.objects.filter(title__icontains='coffee')  # i before contains to make it case sensetive
#     # queryset = Product.objects.filter(description__isnull=True)  # all the product that without description
#     # queryset = Customer.objects.filter(email__icontains='.com')
#     # queryset = Product.objects.filter(inventory__lt=10, unit_price__lt=20)

#     #products:inventory < 10 or unit_price < 20 using query
#     # queryset = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))  # we can add ~ before Q to get the opposite
#     # queryset = Product.objects.filter(inventory= F('collection__id'))   # F helps to compare between the inventory and collection id

#     # queryset = Product.objects.order_by('unit_price', '-title')   # sorting method, when we placed - before title it means we need it in descending order if we add .reverse() after it than we will sor in descending order 
#     # queryset = Product.objects.order_by('unit_price')[0]  # sort in ascending order the unit price and then return the first elemet
#     # queryset = Product.objects.earlies('unit_price')  # same as the one before sort and return the first one or we can use latest()
#     # queryset = Product.objects.all()[:5]  # getting the first 5 from the products 
#     # we can use the query set method to create compex query
#     # queryset = Product.objects.values_list('id', 'title', 'collection__title')   # to get just the id and title
#     # Id = OrderItem.objects.values('product_id').distinct()  # .distinct() to remove the reputation of values
#     # queryset = Product.objects.filter(id__in=Id).order_by('title')   # we linked each product with his Id and then we sort ascending based on the title
#     # queryset = Product.objects.only('id', 'title')   # only method we get instance of the product class while the values_of will get dictionary of products
#     # queryset = Product.objects.differ('description')  # it will keep description un touchable for latter on

#     # we use prefetch_related when we have one to many, each product has one collection and each collection can has many promotions
#     queryset = Product.objects.prefetch_related('promotions').select_related('collection').all()

# get the last 5 orders with their customer and items 

    # queryset = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
    # queryset = Product.objects.aggregate(count = Count('id'), min_price = Min('unit_price')) # how many product do we have
    # queryset = Order.objects.aggregate(count = Count('id'))  # how many Orders do we have
    # queryset = OrderItem.objects.filter(product__id = 1).aggregate(units_sold = Sum('quantity'))
    # queryset = Order.objects.filter(customer__id = 1).aggregate(count_order = Count('id'))  # count how many times customer 1 ordered   
    # queryset = Product.objects.filter(collection__id = 3).aggregate(min =  Min('unit_price'), max =  Max('unit_price'), Avg = Avg('unit_price'))## min, max and average price in collection 3
    # queryset = Customer.objects.annotate(new_id = F('id') + 1)  ## we created new column (new_id) and we set it equal to id + 1   to reference a filled we use F 
    # queryset = Customer.objects.annotate(full_name=Func(F('first_name'), Value(' '), F('last_name'), function = 'CONCAT'))  #Value is for spacing between first and last
    # or 
    # queryset = Customer.objects.annotate(full_name= Concat('first_name', Value(' '), 'last_name' ))
    # queryset = Customer.objects.annotate(count_order =  Count('order'))
    # we use Expressionwrapper with complex function
    # discount  = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField()) 
    # queryset = Product.objects.annotate(discount_price = discount)

    # Top 5 best selling products and their total sales

    # queryset = Product.objects.annotate(total_sales = Sum(F('orderitem__unit_price') * F('orderitem__quantity'))).order_by('-total_sales')[:5]
    # content_type  = ContentType.objects.get_for_model(Product)
    # queryset =  TaggedItem.objects.select_related('tag').filter(content_type=content_type, object_id=1)

    # inserting a new collection 

    # collection =  Collection()
    # collection.title = 'video games'
    # collection.featured_product = Product(pk = 1)
    # collection.save()
    # collection.id
    # Collection.objects.filter(id = 1).delete()
    with transaction.atomic():
        order =  Order()
        order.customer_id =  1
        order.save()

        item = OrderItem()
        item.order = order
        item.product_id =  1
        item.quantity = 1
        item.unit_price = 10
        item.save()

    # transaction is the way or method to make sure if order or orderitem is missing, it will not execute 
  
      
    # Pull data from DataBase
    # Transform
    # Send emails
    return render(request, "hello.html", {'name': 'Mohammad', 'products': queryset})

    