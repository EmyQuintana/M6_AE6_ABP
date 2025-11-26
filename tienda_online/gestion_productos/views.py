from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import View, ListView
from django.contrib import messages
from .forms import ProductoForm
from .models import Producto

def index(request):
    return render(request, 'gestion_productos/index.html')

def registrar_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group_name = request.POST.get('group', 'Gestores de Productos')
            
            try:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
            except Group.DoesNotExist:
                messages.warning(request, f"El grupo '{group_name}' no existe.")

            login(request, user)
            messages.success(request, 'Usuario registrado exitosamente')
            return redirect('index')
    else:
        form = UserCreationForm()

    return render(request, 'gestion_productos/registrar_usuario.html', {'form': form})

def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = AuthenticationForm()
        
    return render(request, 'gestion_productos/login.html', {'form': form})

def logout_usuario(request):
    logout(request)
    return redirect('login_usuario') 

class AgregarProducto(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'gestion_productos.add_producto'
    form_class = ProductoForm
    template_name = 'gestion_productos/crear_producto.html'
    
    # Si no tiene permiso, redirige o lanza 403
    login_url = '/login/' 
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado exitosamente')
            return redirect('listar_productos')
        return render(request, self.template_name, {'form': form})

class ListarProductos(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Vista para ver la lista. Requiere permiso 'view_producto'."""
    permission_required = 'gestion_productos.view_producto'
    model = Producto
    template_name = 'gestion_productos/listar_productos.html'
    context_object_name = 'productos'

class EditarProducto(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Vista para editar. Requiere permiso 'change_producto'."""
    permission_required = 'gestion_productos.change_producto'
    form_class = ProductoForm
    template_name = 'gestion_productos/editar_producto.html'

    def get(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        form = self.form_class(instance=producto)
        return render(request, self.template_name, {'form': form, 'producto': producto})

    def post(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        form = self.form_class(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado correctamente')
            return redirect('listar_productos')
        return render(request, self.template_name, {'form': form, 'producto': producto})

class EliminarProducto(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Vista para eliminar. Requiere permiso 'delete_producto' (Solo Admins)."""
    permission_required = 'gestion_productos.delete_producto'
    template_name = 'gestion_productos/eliminar_producto.html'

    def get(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        return render(request, self.template_name, {'producto': producto})

    def post(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente')
        return redirect('listar_productos')

# --- MANEJo DE ERRORES---

def handler403(request, exception=None):
    """Manejador personalizado para errores 403 (Permiso denegado)"""
    return render(request, 'gestion_productos/403.html', status=403)

def handler404(request, exception=None):
    """Manejador personalizado para errores 404 (Página no encontrada)"""
    return render(request, 'gestion_productos/404.html', status=404)