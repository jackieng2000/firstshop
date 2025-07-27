from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('shop.urls', namespace='shop')),
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('shop1/', include('shop1.urls', namespace='shop1')),
    path('shop2/', include('shop2.urls', namespace='shop2')),
    path('shop3/', include('shop3.urls', namespace='shop3')),
    path('shop4/', include('shop4.urls', namespace='shop4')),
    path('accounts/',include('accounts.urls', namespace='accounts'))
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
