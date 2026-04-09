from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from django.http import HttpResponse

## home page
def home(request):
    ## return render(request, 'home.html')
    return HttpResponse('<h1>Home page </h1>')

'''
AuthenticationController Views. 
'''
## register page
def register(request):
    ## return render(request, 'home.html')
    return HttpResponse('<h1>register page </h1>')
#login page
def login_view(request):
    ## return render(request, 'home.html)
    return HttpResponse('<h1>login page</h1>')
#logout page
def logout_view(request):
    ## return render(request, 'home.html)
    return HttpResponse('<h1>logout page</h1>')

'''
Catalog Views
'''
def catalog(request):
    ## return render(request, 'home.html')
    return HttpResponse('<h1>catalog page</h1>')

'''
ListingController Views
'''
## individual lisitng
def listing_detail(request):
    ## return render(request, 'home.html')
    return HttpResponse('<h1>listing page </h1>')

'''
CartController Views
'''
## cart page
def cart(request):
    ## return render(request, 'home.html')
    return HttpResponse('<h1>cart page </h1>')
def add_to_cart(request):
    ## return render(request, 'home.html')
    return HttpResponse('<h1>add to cart page</h1>')
def remove_from_cart(request):
    ## return render(request, 'home.html')
    return HttpResponse('<h1>remove from cart page</h1>')
def update_cart_quantity(request):
    ## return render(request, 'home.html')
    return HttpResponse('<h1>update cart quantity page</h1>')

'''
Orders Views
'''
## checkout page
def order_history(request):
    ## return render(request, 'home.html')
    return HttpResponse('<h1>order_history</h1>')
def order_detail(request):
    ## return render(request, 'home.html')
    return HttpResponse('<h1>order details page</h1>')
## checkout page
def cancel_order(request):
    ## return render(request, 'home.html')
    return HttpResponse('<h1>cancel order page</h1>')

'''
Checkout Views
'''
## checkout page
def checkout(request):
    ## return render(request, 'home.html')
    return HttpResponse('<h1>checkout page </h1>')
def order_confirmation(request):
    ## return render(request, 'home.html')
    return HttpResponse('<h1>order confirmation page</h1>')

'''
Admin Dashboard Views
'''
def admin_dashboard(request):
    ## return render(request, 'home.html')
    return HttpResponse('<h1>admin dash apge</h1>')
def create_listing(request):
    ## return render(request, 'home.html')
    return HttpResponse('<h1>create listing</h1>')
def edit_listing(request):
    ## return render(request, 'home.html')
    return HttpResponse('<h1>edit listing</h1>')
def remove_listing(request):
    ## return render(request, 'home.html')
    return HttpResponse('<h1>remove lisitng</h1>')
def all_orders(request):
    ## return render(request, 'home.html')
    return HttpResponse('<h1>all ordres</h1>')
def update_order_status(request):
    ## return render(request, 'home.html')
    return HttpResponse('<h1>update order status</h1>')
def update_tracking(request):
    ## return render(request, 'home.html')
    return HttpResponse('<h1>update tracking</h1>')

