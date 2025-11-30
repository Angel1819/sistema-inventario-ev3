from django.shortcuts import render
from .models import Producto, Categoria

# Create your views here.
def inventario_home(request):
    titulo = "Inventario de Productos"
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'inventario_home.html', {
        'titulo': titulo,
        'productos': productos,
        'categorias': categorias
        })