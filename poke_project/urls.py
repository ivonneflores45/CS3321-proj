from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('poke_shop.urls')),
    path('register/', include('poke_shop.urls')),
    path('catalog/', include('poke_shop.urls')),
    path('cart/', include('poke_shop.urls')),
    path('checkout/',include('poke_shop.urls'))
]