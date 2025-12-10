from django.db import models
from django.contrib.auth.models import User  # Para la venta


# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

        class Meta:
            verbose_name = "Categoría"
            verbose_name_plural = "Categorías"


class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    nombre_contacto = models.CharField(max_length=100, blank=True)
    telefono_contacto = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.nombre

        class Meta:
            verbose_name = "Proveedor"
            verbose_name_plural = "Proveedores"


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    stock_minimo = models.PositiveIntegerField(default=5)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    proveedores = models.ManyToManyField('Proveedor', blank=True)

    def __str__(self):
        return self.nombre + ' - ' + self.categoria.nombre

        class Meta:
            verbose_name = "Producto"
            verbose_name_plural = "Productos"


# ═══════════════════════════════════════════════════════════════
# NUEVO: Modelo Carrito (temporal, en sesión)
# ═══════════════════════════════════════════════════════════════

class CarritoItem(models.Model):
    """
    Representa un producto en el carrito
    Se borra cuando se realiza la venta
    """
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    # ↑ Cada carrito pertenece a un usuario
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    # ↑ Referencia al producto
    
    cantidad = models.PositiveIntegerField(default=1)
    # ↑ Cuántos de este producto hay en el carrito
    
    precio_unitario = models.PositiveIntegerField()
    # ↑ Precio del producto cuando se agregó (por si cambia después)
    
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    # ↑ Cuándo se agregó al carrito
    
    def subtotal(self):
        # Método para calcular el subtotal de este item
        # cantidad * precio_unitario
        return self.cantidad * self.precio_unitario
    
    def __str__(self):
        return f"{self.producto.nombre} x{self.cantidad}"

        class Meta:
            verbose_name = "Item del Carrito"
            verbose_name_plural = "Items del Carrito"


# ═══════════════════════════════════════════════════════════════
# NUEVO: Modelo Venta
# ═══════════════════════════════════════════════════════════════

class Venta(models.Model):
    """
    Representa una venta realizada
    Guarda el historial de ventas
    """
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # ↑ Quién realizó la venta
    
    total = models.PositiveIntegerField()
    # ↑ Total de la venta
    
    fecha_venta = models.DateTimeField(auto_now_add=True)
    # ↑ Cuándo se realizó
    
    def __str__(self):
        return f"Venta #{self.id} - ${self.total}"

        class Meta:
            verbose_name = "Venta"
            verbose_name_plural = "Ventas"


# ═══════════════════════════════════════════════════════════════
# NUEVO: Modelo DetalleVenta
# ═══════════════════════════════════════════════════════════════

class DetalleVenta(models.Model):
    """
    Detalles de cada producto en una venta
    """
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    # ↑ A qué venta pertenece
    
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    # ↑ Qué producto se vendió
    
    cantidad = models.PositiveIntegerField()
    # ↑ Cuántos se vendieron
    
    precio_unitario = models.PositiveIntegerField()
    # ↑ A qué precio se vendió
    
    subtotal = models.PositiveIntegerField()
    # ↑ cantidad * precio
    
    def __str__(self):
        return f"{self.producto.nombre} x{self.cantidad}"

        class Meta:
            verbose_name = "Detalle de Venta"
            verbose_name_plural = "Detalles de Ventas"
