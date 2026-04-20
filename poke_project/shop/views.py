# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Listing, Customer, Order, OrderItems, Payment, ShippingInfo
from .filters import ListingFilter
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden


from django.http import HttpResponse

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
            Customer.objects.create(user=user)
            login(request, user) #log em in immediately after registering
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
                return redirect ('admin:index')
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
Author(s): Matt Alvarez
Date created: 4/12/2026
'''
@login_required(login_url='shop-login')
def order_history(request):
    """Display all orders fro the logged-in customer."""
    customer = get_object_or_404(Customer, user=request.user)
    orders = Order.objects.filter(customer=customer).order_by('-order_date')

    return render(request, 'orders/order_history.html', {
        'orders':orders
    })

@login_required(login_url='shop-login')
def order_detail(request):
    """Display details of a specific order."""
    customer = get_object_or_404(Customer, user=request.user)
    order = get_object_or_404(Order, id=id, customer=customer)
    order_items = OrderItems.objects.filter(order=order)
    shipping = ShippingInfo.objects.filter(order=order).first() #returns None if not found
    payment = Payment.objects.filter(order=order).first() #returns None if not found
    
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'order_items': order_items,
        'shipping': shipping,
        'payment': payment
    })

@login_required(login_url='shop-login')
def cancel_order(request):
    """Cancel an order if it's still pending."""
    customer = get_object_or_404(Customer, user=request.user)
    order = get_object_or_404(Order, id=id, customer=customer)

    #only allow cancellation of pending orders
    if order.status != 'pending':
        return HttpResponseForbidden("Only pending orders can be cancelled.")

    if request.method == 'POST':
        order.status = 'cancelled'
        order.save()

        # restore stock
        order_items = OrderItems.objects.filter(order=order)
        for item in order_items:
            listing = item.listing
            listing.stock_quantity += item.quantity
            if listing.listing_status == 'sold':
                listing.listing_status = 'active'
            listing.save()

        return redirect('shop-orders')

    return render(request, 'orders/cancel_order.html', {
        'order': order
    })

'''
Checkout Views
Author(s): Jasmine Zamarron
Date created: 4/19/2026
'''
## checkout page
@login_required(login_url='shop-login')
def checkout(request):
    cart = request.session.get('cart', {})
    #check if empty
    if not cart:
        return redirect('shop-cart')
    
    customer = Customer.objects.get(user=request.user)
    cart_items = []
    total = 0

    for listing_id, quantity in cart.items():
        #calculate total cost
        listing = get_object_or_404(Listing, id=listing_id)
        subtotal = listing.base_price * quantity
        total += subtotal
        #add item details to cart_items
        cart_items.append({
            'listing': listing,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    #mock transaction begins 
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

    #create the order
    order = Order.objects.create(
        customer=customer,
        total_amount = total,
        status='pending'
    )

    #create order items and decrement stock
    for item in cart_items:
        OrderItems.objects.create(
            order=order,
            listing=item['listing'],
            quantity=item['quantity'],
            unit_price=item['listing'].base_price
        )
        item['listing'].stock_quantity -= item['quantity']
        if item['listing'].stock_quantity <= 0:
            item['listing'].listing_status = 'sold'
        item['listing'].save()

    #mock payment
    Payment.objects.create(
        order=order,
        amount=total,
        payment_method=payment_method,
        paymnet_status='completed',
        transaction_id='MOCK-TRANSACTION'
    )

    #create shipping record
    ShippingInfo.objects.create(
        customer=customer,
        order=order,
        recipient_name=request.POST.get('recipient_name', ''),
        address_line1=request.POST.get('address_line1',''),
        address_line2=request.POST.get('address_line2',''),
        city=request.POST.get('city', ''),
        state=request.POST.get('state', ''),
        zip_code=request.POST.get('zip_code', ''),
        country = request.POSt.get('country', ''),
        shipping_status='processing'
    )

    #update order status and clear cart
    order.status = 'processing'
    order.save()
    request.session['cart']= {}

    return redirect('shop-order-confirmation', id=order.id)

#order confirmation 
@login_required(login_url='shop-login')
def order_confirmation(request):
    order = get_object_or_404(Order, id=id, customer__user=request.user)
    return render(request, 'checkout/order_confirmation.html', {'order':order})


