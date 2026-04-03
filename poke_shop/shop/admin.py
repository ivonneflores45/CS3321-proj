from django.contrib import admin
from .models import Customer, Listing, Order, OrderItems, Payment, ShippingInfo

# Register your models here.
admin.site.register(Customer)
admin.site.register(Listing)
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(Payment)
admin.site.register(ShippingInfo)



