from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User


# Register this model on admin
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

#Create an orderitem inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem

#Extend our order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [OrderItemInline]

#Unregister order model
admin.site.unregister(Order)

#Re-register order and order admin
admin.site.register(Order, OrderAdmin)