from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock']
        
        labels = {
            'nombre': 'Nombre del Producto',
            'descripcion': 'Descripción Detallada',
            'precio': 'Precio Unitario ($)',
            'stock': 'Unidades en Inventario',
        }
      
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej: Monitor 24"'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Ingrese detalles técnicos...'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',  
                'step': '0.01'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'   
            }),
        }

    def clean_precio(self):
        """Valida que el precio no sea negativo."""
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio < 0:
            raise forms.ValidationError("El precio no puede ser un valor negativo.")
        return precio

    def clean_stock(self):
        """Valida que el stock no sea negativo."""
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise forms.ValidationError("El stock no puede ser negativo.")
        return stock