from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Producto, Categoria
from .forms import CategoriaForm, ProductoForm, ProveedorForm

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
    
def editar_producto(request, id):
    # Obtener el producto por su ID o mostrar error 404 si no existe
    producto = get_object_or_404(Producto, id=id)
    
    if request.method == 'POST':
        # Rellenar el formulario con los datos enviados Y la instancia del producto
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()  # Actualiza el producto existente
            messages.success(request, 'Producto actualizado exitosamente')
            return redirect('inventario_home')
    else:
        # Prellenar el formulario con los datos actuales del producto
        form = ProductoForm(instance=producto)
    
    return render(request, 'inventario/editar_producto.html', {
        'form': form,
        'producto': producto
    })
    
def eliminar_producto(request, id):
    # Obtener el producto o mostrar error 404
    producto = get_object_or_404(Producto, id=id)
    
    if request.method == 'POST':
        # Solo eliminar si se confirma con POST (seguridad)
        producto.delete()
        messages.success(request, f'Producto "{producto.nombre}" eliminado exitosamente')
        return redirect('inventario_home')
    
    # Mostrar página de confirmación
    return render(request, 'inventario/eliminar_producto.html', {
        'producto': producto
    })
    
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario_home')
    else:
        form = CategoriaForm()
        
    return render(request, 'inventario/crear_categoria.html', {
        'form': form
    })
    
def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario_home')
    else:
        form = ProveedorForm()
    
    return render(request, 'inventario/crear_proveedor.html', {
        'form': form
    })
