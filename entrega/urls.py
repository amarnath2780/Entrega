
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin1/', admin.site.urls),
    path('', include('accounts.urls')),
    path('store/' , include('store.urls')),
    path('admin/' , include('superuser.urls')),
    path('cart/' , include('cart.urls')),
    path('order/' , include('order.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
