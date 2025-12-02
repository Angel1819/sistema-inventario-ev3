from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventario_home, name='inventario_home'),
    path('crear_producto/', views.crear_producto, name='crear_producto'),
    path('editar_producto/<int:id>/', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('crear_categoria/', views.crear_categoria, name='crear_categoria'),
    path('crear_proveedor/', views.crear_proveedor, name='crear_proveedor'),
]
