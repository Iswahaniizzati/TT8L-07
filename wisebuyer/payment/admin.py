from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem


# Register this model on admin
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)