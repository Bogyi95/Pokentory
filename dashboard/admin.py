from django.contrib import admin
from .models import Product, Order, Category
from django.contrib.auth.models import Group

admin.site.site_header = 'Inventory Dashboard'

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_list', 'quantity')
    list_filter = ['category']

    def category_list(self, obj):
        return ", ".join([c.name for c in obj.category.all()])
    category_list.short_description = 'Categories'

    
# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(Category)
# admin.site.unregister(Group)