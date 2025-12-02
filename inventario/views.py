from django.shortcuts import render, redirect
from .models import Producto, Categoria
from .forms import CategoriaForm, ProductoForm

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
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario_home')
    else:
        form = ProductoForm()
    
    return render(request, 'inventario/crear_producto.html', {
        'form': form
    })
    
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crear_producto')
    else:
        form = CategoriaForm()
        
    return render(request, 'inventario/crear_categoria.html', {
        'form': form
    })
