import os
import sys
import django

# --- 1. CONFIGURACIÓN DEL ENTORNO ---

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root) 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda_online.settings')
django.setup()

from django.contrib.auth.models import Group, Permission, User

def crear_grupos():
    
    print("=== CREANDO GRUPOS DE USUARIOS (TIENDA ONLINE) ===")
    
    grupos = {
        'Gestores de Productos': [
            'view_producto',    
            'add_producto',     # Agregar
            'change_producto'   # Editar (SIN ELIMINAR)
        ],
        'Administradores': [
            'view_producto', 
            'add_producto', 
            'change_producto', 
            'delete_producto'  
        ]
    }
    
    for nombre_grupo, permisos in grupos.items():
        grupo, creado = Group.objects.get_or_create(name=nombre_grupo)
        estado = "creado" if creado else "ya existe"
        print(f"✓ Grupo '{nombre_grupo}' {estado}")
            
        # Asignar permisos
        for codigo_permiso in permisos:
            try:
                permiso = Permission.objects.get(codename=codigo_permiso)
                grupo.permissions.add(permiso)
                print(f"  - Permiso '{codigo_permiso}' asignado")
            except Permission.DoesNotExist:
                print(f"  ✗ ERROR: El permiso '{codigo_permiso}' no existe. Verifica el nombre del modelo.")
    
    # --- CREACIÓN DE USUARIOS DE PRUEBA (Opcional pero recomendado) ---
    print("\n=== VERIFICANDO USUARIOS DE PRUEBA ===")
    crear_usuario('admin_tienda', 'admin123', 'Administradores')
    crear_usuario('gestor_tienda', 'gestor123', 'Gestores de Productos')

def crear_usuario(username, password, nombre_grupo):
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username=username, password=password)
        user.is_staff = True # Necesario para entrar al admin
        grupo = Group.objects.get(name=nombre_grupo)
        user.groups.add(grupo)
        user.save()
        print(f"✓ Usuario '{username}' creado y asignado a '{nombre_grupo}'")
    else:
        print(f"✓ Usuario '{username}' ya existe")

if __name__ == "__main__":
    crear_grupos()