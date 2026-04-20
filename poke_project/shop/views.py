# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Listing, Order, OrderItems, Payment, ShippingInfo, Customer
from .filters import ListingFilter
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Customer
from django.contrib.auth.models import User


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

## home page
def home(request):
    return render(request, 'home.html')

'''
AuthenticationController Views. 
Author(s): Matt A
Date created: 4/10/2026
'''
## register page
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(user=user)
            login(request, user) 
            return redirect('shop-home')    
    else:
        form = UserCreationForm()

    return render(request, 'auth/register.html', {'form':form})

#login page
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect ('shop-dashboard')
            return redirect('shop-catalog')
    else:
        form = AuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})

#logout page
def logout_view(request):
    logout(request) #clear session automatically
    return redirect ('auth/logout.html')


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
Author(s): Maryam Khan
Date created: 4/11/2026
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
Matt Alvarez
'''
## checkout page
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('shop-cart')
    if request.method == 'POST':
    # Collect info
        recipient_name = request.POST.get('recipient_name')
        address = request.POST.get('address')  
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        country = request.POST.get('country')  
        payment_method = request.POST.get('payment_method')

        customer = Customer.objects.get(user=request.user)
        total = customer.total_amount #function to calculate total from cart items
        order = Order.objects.create(customer=customer, total_amount=total ) 


        for listing_id, quantity in cart.items():
            listing = get_object_or_404(Listing, id=listing_id)
            OrderItems.objects.create(
                order=order,
                listing=listing,
                quantity=quantity,
                unit_price=listing.base_price
            )
        ShippingInfo.objects.create(
            customer=Customer,
            order=order,
            recipient_name=recipient_name,
            address_line1=address,
            city=city,
            state=state,
            zipcode=zip_code,
            country=country
        )

        Payment.objects.create(
            order=order,
            amount=total,
            payment_method=payment_method,
            payment_status='completed',
        )
        request.session['cart'] = {}
        return redirect('shop-order-confirmation')
    
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
    return render(request, 'checkout/checkout.html', {
        'cart_items':cart_items,
        'total':total,
    })  

















def order_confirmation(request):

    Customer.objects.get(user=request.user)
    order = Order.objects.filter(customer=Customer).latest('order_date')
    order_items = OrderItems.objects.filter(order=order)
    shipping = ShippingInfo.objects.get(order=order)

    return render(request, 'checkout/order_confirmation.html', {
        'order': order,
        'order_items': order_items,
        'shipping': shipping
    }   )

'''
Admin Dashboard Views
'''
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('shop-login')
        return view_func(request, *args, **kwargs)
    return wrapper
@admin_required
def admin_dashboard(request):
    total_orders = Order.objects.count()
    total_revenue = Payment.objects.filter(payment_status='completed').aggregate(total=models.Sum('amount'))['total'] or 0
    total_listings = Listing.objects.count()
    active_listings = Listing.objects.filter(listing_status='active').count()

    return render(request, 'admin/admin_dashboard.html', {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_listings': total_listings,
        'active_listings': active_listings
    }   )
@admin_required
def create_listing(request):
    if request.method == 'POST':
        listing = Listing.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            base_price=request.POST.get('base_price'),
            stock_quantity=request.POST.get('stock_quantity'),
            category=request.POST.get('category'),
            condition=request.POST.get('condition'),
            rarity=request.POST.get('rarity'),
            element=request.POST.get('element'),
            type=request.POST.get('type'),
            set_name=request.POST.get('set_name'),
            image = request.FILES.get('image')
        )

        return redirect('shop-dashboard')
    return render(request, 'admin/create_listing.html')
@admin_required
def edit_listing(request):
    return render(request, 'admin/edit_listing.html')
@admin_required
def remove_listing(request):
    return render(request, 'admin/remove_listing.html')
def all_orders(request):
    return render(request, 'admin/all_orders.html')
def update_order_status(request):
    return render(request, 'admin/update_order_status.html')
def update_tracking(request):
    return render(request, 'admin/update_tracking.html')

