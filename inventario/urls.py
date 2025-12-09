# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.inventario_home, name='inventario_home'),
#     path('crear_producto/', views.crear_producto, name='crear_producto'),
#     path('editar_producto/<int:id>/', views.editar_producto, name='editar_producto'),
#     path('eliminar_producto/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
#     path('crear_categoria/', views.crear_categoria, name='crear_categoria'),
#     path('crear_proveedor/', views.crear_proveedor, name='crear_proveedor'),
# ]
from django.urls import path
from . import views

urlpatterns = [
    # Inventario
    path('', views.inventario_home, name='inventario_home'),
    
    # Productos
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/<int:id>/editar/', views.editar_producto, name='editar_producto'),
    path('productos/<int:id>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
    
    # Categorías
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
    
    # Proveedores
    path('proveedores/crear/', views.crear_proveedor, name='crear_proveedor'),
    
    # ═══════════════════════════════════════════════════════════════
    # CARRITO
    # ═══════════════════════════════════════════════════════════════
    
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    # URL: /carrito/  |  Para ver el carrito
    
    path('carrito/agregar/<int:id>/', views.agregar_carrito, name='agregar_carrito'),
    # URL: /carrito/agregar/5/  |  Para agregar producto con ID 5
    
    path('carrito/<int:id>/aumentar/', views.aumentar_cantidad, name='aumentar_cantidad'),
    # URL: /carrito/1/aumentar/  |  Para aumentar cantidad del item 1
    
    path('carrito/<int:id>/disminuir/', views.disminuir_cantidad, name='disminuir_cantidad'),
    # URL: /carrito/1/disminuir/  |  Para disminuir cantidad del item 1
    
    path('carrito/<int:id>/eliminar/', views.eliminar_carrito, name='eliminar_carrito'),
    # URL: /carrito/1/eliminar/  |  Para eliminar item 1 del carrito
    
    path('venta/realizar/', views.realizar_venta, name='realizar_venta'),
    # URL: /venta/realizar/  |  Para confirmar y realizar la venta
]
