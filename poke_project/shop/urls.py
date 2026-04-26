"""
URL configuration for poke_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

'''
shop/urls.py
authors: Maryam & Ivonne
date-started: 5/6/2026; Ivonne
date-finished: 5/7/2026; Maryam
'''
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    ## default = home page
    path('', views.home, name='shop-home'),

    #registration, login, & logout
    path('register/', views.register, name='shop-register'),
    path('login/', views.login_view, name='shop-login'),
    path('logout/', views.logout_view, name='shop-logout'),

    #catalog
    path('catalog/', views.catalog, name='shop-catalog'),

    #individual listing page
    path('listing/<int:id>/', views.listing_detail, name='shop-listing'),

    #cart actions
    path('cart/', views.cart, name='shop-cart'),
    path('cart/add/<int:id>/', views.add_to_cart, name='cart-add'),
    path('cart/remove/<int:id>/', views.remove_from_cart, name='cart-remove'),
    path('cart/update/<int:id>/', views.update_cart_quantity, name='cart-update'),

    #orders
    path('orders/', views.order_history, name='shop-orders'),
    path('orders/<int:id>/', views.order_detail, name='shop-order-detail'),
    path('orders/<int:id>/cancel/', views.cancel_order, name='shop-order-cancel'),

    #checkout
    path('checkout/checkout/', views.checkout, name='shop-checkout'),
    path('orders/<int:id>/confirmation/', views.order_confirmation, name='shop-order-confirmation'),

    #admin dashboard
    # path('dashboard/', views.admin_dashboard, name='shop-dashboard'),
    # path('dashboard/listings/create/', views.create_listing, name='shop-listing-create'),
    # path('dashboard/listings/<int:id>/edit/', views.edit_listing, name='shop-listing-edit'),
    # path('dashboard/listings/<int:id>/remove/', views.remove_listing, name='shop-listing-remove'),
    # path('dashboard/orders/', views.all_orders, name='shop-all-orders'),
    # path('dashboard/orders/<int:id>/status/', views.update_order_status, name='shop-order-status'),
    # path('dashboard/shipping/<int:id>/tracking/', views.update_tracking, name='shop-tracking'),
]
