# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Listing, Customer
from .filters import ListingFilter

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

## home page
def home(request):
    return render(request, 'home.html')

'''
AuthenticationController Views. 
Author(s): Matt Alvarez
Date created: 4/10/2026
'''
## register page
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(user=user)  # Create associated Customer profile
            login(request, user)
        return redirect('shop-home')
    else:
        form = UserCreationForm()

    return render(request, 'auth/register.html', {'form': form})

#login page
def login_view(request):
    next_url = request.GET.get('next', 'shop-home')  # Default to home if no next parameter
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect('shop-dashboard')  # Redirect admins to dashboard
            return redirect('shop-home')
    else:
        form = AuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})


#logout page
def logout_view(request):
    logout(request)
    return redirect('shop-home')


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
'''

def _get_cart(request):
    return request.session.get('cart', {})


def _save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def _build_cart_items(request):
    cart = _get_cart(request)
    items = []
    total = 0
    if not cart:
        return items, total

    listing_ids = [int(pk) for pk in cart.keys()]
    listings = Listing.objects.filter(pk__in=listing_ids)
    for listing in listings:
        quantity = cart.get(str(listing.id), 0)
        subtotal = listing.base_price * quantity
        total += subtotal
        items.append({'listing': listing, 'quantity': quantity, 'subtotal': subtotal})

    return items, total


## individual listing
def listing_detail(request, id):
    listing = get_object_or_404(Listing, pk=id, listing_status='active')
    return render(request, 'listing_detail.html', {'listing': listing})


'''
CartController Views
'''
## cart page
def cart(request):
    cart_items, cart_total = _build_cart_items(request)
    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
    })


def add_to_cart(request):
    if request.method == 'POST':
        listing_id = request.POST.get('listing_id')
        quantity = int(request.POST.get('quantity', 1))
        listing = get_object_or_404(Listing, pk=listing_id, listing_status='active')

        cart = _get_cart(request)
        key = str(listing.id)
        cart[key] = cart.get(key, 0) + max(quantity, 1)
        cart[key] = min(cart[key], listing.stock_quantity)
        _save_cart(request, cart)

        return redirect('shop-cart')

    return render(request, 'cart/cart_add.html')


def remove_from_cart(request, id):
    cart = _get_cart(request)
    cart.pop(str(id), None)
    _save_cart(request, cart)
    return redirect('shop-cart')


def update_cart_quantity(request, id):
    listing = get_object_or_404(Listing, pk=id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = _get_cart(request)
        if quantity <= 0:
            cart.pop(str(id), None)
        else:
            cart[str(id)] = min(quantity, listing.stock_quantity)
        _save_cart(request, cart)
        return redirect('shop-cart')

    return render(request, 'cart/update_cart_quantity.html', {'listing': listing})

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

