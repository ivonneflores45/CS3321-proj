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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    ## default = home page
    # path('', views.home, name='shop-home'),

    # path('register/', views.register, name='shop-register'),
    # path('catalog/', views.catalog, name='shop-catalog'),
    # path('cart/', views.cart, name='shop-cart'),
    # path('checkout/', views.checkout, name='shop-checkout'),

    # #login and logout
    # path('login/', views.login_view, name='shop-login'),
    # path('logout/', views.logout_view, name='shop-logout'),

    # #individual listing page
    # path('listing/<int:id>/', views.listing_detail, name='shop-listing'),

    # #cart actions
    # path('cat/add/',)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
