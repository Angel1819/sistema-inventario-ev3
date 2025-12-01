from django import forms
from .models import Producto, Categoria

class ProductoForm(forms.ModelForm):
    # Personalizaciones opcionales para mejor UX
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label='Descripción',
        required=False
    )
    
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'categoria', 'precio', 'stock']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
