from django.contrib import admin
from .models import Producto, Categoria, Proveedor, CarritoItem, Venta, DetalleVenta


# ═══════════════════════════════════════════════════════════════
# Configuración personalizada del Admin
# ═══════════════════════════════════════════════════════════════

class VentaAdmin(admin.ModelAdmin):
    """
    Personaliza cómo se muestra Venta en el admin
    """
    list_display = ['id', 'usuario', 'total', 'fecha_venta']
    # ↑ Columnas que se verán en la lista
    
    list_filter = ['fecha_venta', 'usuario']
    # ↑ Filtros laterales
    
    search_fields = ['usuario__username']
    # ↑ Buscar por nombre de usuario
    
    readonly_fields = ['fecha_venta']
    # ↑ La fecha no se puede editar manualmente


class DetalleVentaAdmin(admin.ModelAdmin):
    """
    Personaliza cómo se muestra DetalleVenta en el admin
    """
    list_display = ['id', 'venta', 'producto', 'cantidad', 'precio_unitario', 'subtotal']
    # ↑ Columnas que se verán en la lista
    
    list_filter = ['venta__fecha_venta', 'producto']
    # ↑ Filtros laterales
    
    search_fields = ['producto__nombre', 'venta__id']
    # ↑ Buscar por nombre de producto o ID de venta


class CarritoItemAdmin(admin.ModelAdmin):
    """
    Personaliza cómo se muestra CarritoItem en el admin
    """
    list_display = ['id', 'usuario', 'producto', 'cantidad', 'precio_unitario', 'fecha_agregado']
    list_filter = ['fecha_agregado', 'usuario']
    search_fields = ['usuario__username', 'producto__nombre']


# Register your models here.
admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Proveedor)
admin.site.register(CarritoItem, CarritoItemAdmin)
admin.site.register(Venta, VentaAdmin)
admin.site.register(DetalleVenta, DetalleVentaAdmin)