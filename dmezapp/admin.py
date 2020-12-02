from django.contrib import admin

from dmezapp.models import Product, Products, newregis, Customer, Order, OrderItem, ShippingAddress
# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Products)
admin.site.register(newregis)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
