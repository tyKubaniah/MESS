from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('django-native-admin/', admin.site.urls),
    path('', include('orders.urls')),
]