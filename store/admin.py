from django.contrib import admin, messages
from django.contrib.contenttypes.admin import GenericTabularInline
from . import models
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from tags.models import TaggedItem




# Register your models here.


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [('<10', 'low')]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt = 10)

class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    inlines = ['TagInline']
    prepopulated_fields = {'slug' : ['title']}
    search_fields = ['title']
    actions = ['clear_inventory']
    list_display =  ['title', 'unit_price', 'inventory_status', 'collection']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update']
    list_per_page = 10

    @admin.display(ordering='inventory_status')
    def inventory_status(self, product):
        if product.inventory < 10 :
            return 'Low'
        return 'Ok'


    @admin.action(description= 'Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory = 0)
        self.message_user(request, f'{updated_count}  Products were successfuly updated', messages.ERROR)


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    # autocomplete_fields = ['order']
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    list_per_page = 10

class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 10
    model = models.OrderItem
    extra = 0



@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    inlines = [OrderItemInline]
    search_fields = ['title']


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):

    list_display = ['title', 'products_count']
    search_fields = ['title']


    
    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (reverse('admin:store_product_changelist') + '?' + urlencode({'collection__id': str(collection.id)}))
        return format_html('<a href="{}">{}</a>', url, collection.products_count)
        

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count = Count('product'))

# admin.site.register(models.Product, ProductAdmin)
# admin.site.register(models.Customer, CustomerAdmin)






