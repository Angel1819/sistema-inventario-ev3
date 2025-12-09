from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Producto, Categoria, CarritoItem, Venta, DetalleVenta
from .forms import CategoriaForm, ProductoForm, ProveedorForm
from usuarios.decorators import rol_requerido, solo_administrador


# ═══════════════════════════════════════════════════════════════
# INVENTARIO HOME (Protegida - Solo logueados)
# ═══════════════════════════════════════════════════════════════

@login_required(login_url='iniciar_sesion')
def inventario_home(request):
    # request.user es el usuario logueado
    
    titulo = "Inventario de Productos"
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    
    return render(request, 'inventario/inventario_home.html', {
        'titulo': titulo,
        'productos': productos,
        'categorias': categorias
    })


# ═══════════════════════════════════════════════════════════════
# CARRITO: Ver carrito
# ═══════════════════════════════════════════════════════════════

@login_required(login_url='iniciar_sesion')
def ver_carrito(request):
    # Obtener todos los items del carrito del usuario logueado
    carrito_items = CarritoItem.objects.filter(usuario=request.user)
    # ↑ Solo los items de este usuario
    
    # Calcular el total
    total = 0
    for item in carrito_items:
        total += item.subtotal()
    # ↑ Sumar todos los subtotales
    
    return render(request, 'inventario/carrito.html', {
        'carrito_items': carrito_items,
        'total': total
    })


# ═══════════════════════════════════════════════════════════════
# CARRITO: Agregar producto al carrito
# ═══════════════════════════════════════════════════════════════

@login_required(login_url='iniciar_sesion')
def agregar_carrito(request, id):
    # id es el ID del producto a agregar
    
    # Obtener el producto
    producto = get_object_or_404(Producto, id=id)
    # ↑ Si no existe, muestra error 404
    
    # Verificar si ya existe en el carrito
    carrito_item = CarritoItem.objects.filter(
        usuario=request.user,
        producto=producto
    ).first()
    # ↑ .first() devuelve el primer item o None si no existe
    
    if carrito_item:
        # ✅ Ya existe en el carrito
        # Aumentar la cantidad en 1
        carrito_item.cantidad += 1
        carrito_item.save()
        # ↑ Guardar los cambios
    else:
        # ❌ No existe en el carrito
        # Crear un nuevo item
        CarritoItem.objects.create(
            usuario=request.user,
            producto=producto,
            cantidad=1,
            precio_unitario=producto.precio
            # ↑ Guardar el precio actual del producto
        )
    
    # Mostrar mensaje
    messages.success(request, f'"{producto.nombre}" agregado al carrito')
    
    # Redirigir al inventario
    return redirect('inventario_home')


# ═══════════════════════════════════════════════════════════════
# CARRITO: Aumentar cantidad
# ═══════════════════════════════════════════════════════════════

@login_required(login_url='iniciar_sesion')
def aumentar_cantidad(request, id):
    # id es el ID del CarritoItem
    
    # Obtener el item del carrito
    carrito_item = get_object_or_404(CarritoItem, id=id, usuario=request.user)
    # ↑ Verificar que pertenece a este usuario
    
    # Aumentar cantidad en 1
    carrito_item.cantidad += 1
    carrito_item.save()
    
    # Redirigir al carrito
    return redirect('ver_carrito')


# ═══════════════════════════════════════════════════════════════
# CARRITO: Disminuir cantidad
# ═══════════════════════════════════════════════════════════════

@login_required(login_url='iniciar_sesion')
def disminuir_cantidad(request, id):
    # id es el ID del CarritoItem
    
    # Obtener el item del carrito
    carrito_item = get_object_or_404(CarritoItem, id=id, usuario=request.user)
    # ↑ Verificar que pertenece a este usuario
    
    # Disminuir cantidad en 1
    carrito_item.cantidad -= 1
    
    if carrito_item.cantidad <= 0:
        # Si la cantidad llega a 0, eliminar el item
        carrito_item.delete()
    else:
        # Si aún queda cantidad, guardar
        carrito_item.save()
    
    # Redirigir al carrito
    return redirect('ver_carrito')


# ═══════════════════════════════════════════════════════════════
# CARRITO: Eliminar producto del carrito
# ═══════════════════════════════════════════════════════════════

@login_required(login_url='iniciar_sesion')
def eliminar_carrito(request, id):
    # id es el ID del CarritoItem
    
    # Obtener el item del carrito
    carrito_item = get_object_or_404(CarritoItem, id=id, usuario=request.user)
    # ↑ Verificar que pertenece a este usuario
    
    # Obtener el nombre del producto para mostrar en el mensaje
    nombre_producto = carrito_item.producto.nombre
    
    # Eliminar el item
    carrito_item.delete()
    
    # Mostrar mensaje
    messages.success(request, f'"{nombre_producto}" eliminado del carrito')
    
    # Redirigir al carrito
    return redirect('ver_carrito')


# ═══════════════════════════════════════════════════════════════
# VENTA: Realizar venta (descontar stock)
# ═══════════════════════════════════════════════════════════════

@login_required(login_url='iniciar_sesion')
def realizar_venta(request):
    # request.user es quien realiza la venta
    
    # Obtener todos los items del carrito
    carrito_items = CarritoItem.objects.filter(usuario=request.user)
    
    if not carrito_items:
        # Si el carrito está vacío
        messages.error(request, 'El carrito está vacío')
        return redirect('ver_carrito')
    
    # Calcular el total
    total = 0
    for item in carrito_items:
        total += item.subtotal()
    
    # Crear la venta
    venta = Venta.objects.create(
        usuario=request.user,
        total=total
    )
    # ↑ Guardamos la venta en la BD
    
    # Para cada item en el carrito
    for item in carrito_items:
        # Crear detalle de venta
        DetalleVenta.objects.create(
            venta=venta,
            producto=item.producto,
            cantidad=item.cantidad,
            precio_unitario=item.precio_unitario,
            subtotal=item.subtotal()
        )
        
        # IMPORTANTE: Descontar stock del producto
        producto = item.producto
        producto.stock -= item.cantidad
        # ↑ Restar la cantidad vendida del stock
        
        if producto.stock < 0:
            # No permitir stock negativo
            producto.stock = 0
        
        producto.save()
        # ↑ Guardar los cambios en el producto
    
    # Eliminar los items del carrito
    carrito_items.delete()
    # ↑ Limpiar el carrito después de la venta
    
    # Mostrar mensaje
    messages.success(request, f'Venta realizada exitosamente. Total: ${total}')
    
    # Redirigir al inventario
    return redirect('inventario_home')


# ═══════════════════════════════════════════════════════════════
# RESTO DE VISTAS (Decoradores añadidos)
# ═══════════════════════════════════════════════════════════════

@solo_administrador
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


@solo_administrador
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente')
            return redirect('inventario_home')
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'inventario/editar_producto.html', {
        'form': form,
        'producto': producto
    })


@solo_administrador
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    
    if request.method == 'POST':
        nombre_producto = producto.nombre
        producto.delete()
        messages.success(request, f'Producto "{nombre_producto}" eliminado exitosamente')
        return redirect('inventario_home')
    
    return render(request, 'inventario/eliminar_producto.html', {
        'producto': producto
    })


@solo_administrador
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


@solo_administrador
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
