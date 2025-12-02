from django import forms
from .models import Producto, Categoria, Proveedor

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'categoria', 'precio', 'stock', 'stock_minimo', 'proveedores']
        labels = {
                'nombre': 'Nombre del Producto',
                'descripcion': 'Descripción detallada',
                'stock_minimo': 'Stock Mínimo',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Unstable Unicorns'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 5'}),
            # SelectMultiple permite seleccionar varios proveedores (mantén Ctrl para múltiple selección)
            'proveedores': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        labels = {
            'nombre': 'Nombre de la Categoría',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Pokémon'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'nombre_contacto', 'telefono_contacto', 'email', 'direccion']
        labels = {
            'nombre': 'Nombre del Proveedor',
            'nombre_contacto': 'Nombre del Contacto',
            'telefono_contacto': 'Teléfono del Contacto',
            'email': 'Correo Electrónico',
            'direccion': 'Dirección Física',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Proveedor S.A.'}),
            'nombre_contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Juan Pérez'}),
            'telefono_contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56 9 1234 5678'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Calle Falsa 123'}),
        }