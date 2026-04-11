# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Listing
from .filters import ListingFilter

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
Author(s): Maryam Khan
Date created: 4/10/2026
notes: template must be updated for filtering. 
'''
def catalog(request):
    listings = Listing.objects.filter(listing_status ='active')
    listing_filter = ListingFilter(request.GET, queryset=listings)
    return render(request, 'catalog.html', {
        'filter': listing_filter,
        'listings': listing_filter.qs #filtered queryset
    })

'''
ListingController Views
Author(s): Maryam Khan
Date created 4/11/2026
'''
## individual lisitng
def listing_detail(request, id):
    listing = get_object_or_404(Listing, id=id, listing_status='active')
    return render(request, 'listing_detail.html', {'listing':listing})


'''
CartController Views
'''
## cart page
def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for listing_id, quantity in cart.items():
        listing = get_object_or_404(Listing, id=listing_id)
        subtotal = listing.base_price * quantity
        total += subtotal
        cart_items.append({
            'listing':listing,
            'quantity':quantity,
            'subtotal':subtotal,
        })

    return render(request, 'cart/cart.html', {
        'cart_items':cart_items,
        'total':total,
    })

def add_to_cart(request,id):
    listing = get_object_or_404(Listing, id=id)
    cart = request.session.get('cart',{})
    str_id = str(id) #session key has to be converted to string

    if str_id in cart:
        cart[str_id] += 1
    else:
        cart[str_id] = 1
    
    request.session['cart'] = cart
    return redirect ('cart/cart_add.html')

def remove_from_cart(request, id):
    cart = request.session.get('cart',{})
    str_id = str(id) #session key has to be converted to string

    if str_id in cart:
        del cart[str_id]

    request.session['cart'] = cart
    return redirect ('cart/remove_from_cart.html')

def update_cart_quantity(request, id):
    cart = request.session.get('cart',{})
    str_id = str(id) #session key has to be converted to string
    quantity = int(request.POST.get('quantity', 1))

    if quantity <= 0:
        del cart[str_id]
    else:
        cart[str_id] = quantity
    
    request.session['cart'] = cart
    return redirect ('cart/update_cart_quantity.html')

'''
Orders Views
'''
def order_history(request):
    return render(request, 'orders/order_history.html')
def order_detail(request):
    return render(request, 'orders/order_detail.html')
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

