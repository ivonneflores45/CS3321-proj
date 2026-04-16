from django.contrib import admin
from .models import Customer, Listing, Order, OrderItems, Payment, ShippingInfo

'''
Updating Django's Dashboard
for PokeBid functionality
Author(s): Maryam Khan
Date created: 4/16/2026
'''
#listing options
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'base_price', 'stock_quantity', 'listing_status']
    list_filter = ['category', 'rarity', 'listing_status']
    search_fields = ['title', 'set_name']
    list_editable = ['listing_status', 'stock_quantity']

#orders
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'order_date', 'total_amount', 'status']
    list_filter = ['status', 'customer']
    list_editable = ['status']

#shipping
class ShippingInfoAdmin(admin.ModelAdmin):
    list_display = ['order', 'recipient_name', 'shipping_status', 'tracking_number']
    list_filter = ['shipping_status', 'recipient_name', 'order']
    list_editable = ['shipping_status', 'tracking_number']

#payment
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'amount', 'payment_method', 'payment_status', 'payment_date']
    list_filter = ['payment_status', 'payment_method']

#order items
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'listing', 'quantity', 'unit_price']


# Register your models here.
admin.site.register(Customer)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItems, OrderItemAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(ShippingInfo, ShippingInfoAdmin)



