from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gestion_productos.urls')), 
]

handler403 = 'gestion_productos.views.handler403'
handler404 = 'gestion_productos.views.handler404'