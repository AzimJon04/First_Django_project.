from django.contrib import admin
# Register your models here.
from .models import Categories, Products, Basket, Orders


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'categories', 'stock', 'data_created')
    search_fields = ('name',)
    list_filter = ('categories',)
    list_editable = ('price', 'stock', 'categories')
    list_per_page = 10
    ordering = ('-data_created',)


class BasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'data_created')


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'data_created')


admin.site.register(Categories)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Basket, BasketAdmin)
admin.site.register(Orders, OrdersAdmin)