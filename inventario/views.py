from django.shortcuts import render
from .models import Producto, Categoria

# Create your views here.
def inventario_home(request):
    titulo = "Inventario de Productos"
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'inventario/inventario_home.html', {
        'titulo': titulo,
        'productos': productos,
        'categorias': categorias
        })
    
def crear_producto(request):
    return render(request, 'inventario/crear_producto.html')
