from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('registro/', views.registrar_usuario, name='registrar_usuario'),
    path('login/', views.login_usuario, name='login_usuario'),
    path('logout/', views.logout_usuario, name='logout_usuario'),

    # (CRUD) ---
    
    path('productos/', views.ListarProductos.as_view(), name='listar_productos'),
    path('productos/crear/', views.AgregarProducto.as_view(), name='agregar_producto'),
    path('productos/editar/<int:pk>/', views.EditarProducto.as_view(), name='editar_producto'),
    path('productos/eliminar/<int:pk>/', views.EliminarProducto.as_view(), name='eliminar_producto'),
] 
