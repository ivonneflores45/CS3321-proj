# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Listing
from .filters import ListingFilter

from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Customer

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

