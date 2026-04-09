# Create your views here.
from django.shortcuts import render

from django.http import HttpResponse

## home page
def home(request):
    return render(request, 'home.html')

'''
AuthenticationController Views. 
'''
## register page
def register(request):
    return render(request, 'auth/register.html')

#login page
def login_view(request):
    return render(request, 'auth/login.html')


#logout page
def logout_view(request):
    return render(request, 'auth/logout.html')


'''
Catalog Views
'''
def catalog(request):
    return render(request, 'catalog.html')

'''
ListingController Views
'''
## individual lisitng
def listing_detail(request):
    return render(request, 'listing.html')


'''
CartController Views
'''
## cart page
def cart(request):
    return render(request, 'cart/cart.html')
def add_to_cart(request):
    return render(request, 'cart/cart_add.html')
def remove_from_cart(request):
    return render(request, 'remove_from_cart.html')
def update_cart_quantity(request):
    return render(request, 'update_cart_quantity.html')

'''
Orders Views
'''
## checkout page
def order_history(request):
    return render(request, 'orders/order_history.html')
def order_detail(request):
    return render(request, 'orders/order_detail.html')
## checkout page
def cancel_order(request):
    return render(request, 'orders/cancel_order.html')

'''
Checkout Views
'''
## checkout page
def checkout(request):
    return render(request, 'checkout/checkout.html')
def order_confirmation(request):
    return render(request, 'checkout/order_confirmation.html')

'''
Admin Dashboard Views
'''
def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')
def create_listing(request):
    return render(request, 'admin/create_listing.html')
def edit_listing(request):
    return render(request, 'admin/edit_listing.html')
def remove_listing(request):
    return render(request, 'admin/remove_listing.html')
def all_orders(request):
    return render(request, 'admin/all_orders.html')
def update_order_status(request):
    return render(request, 'admin/update_order_status.html')
def update_tracking(request):
    return render(request, 'admin/update_tracking.html')

