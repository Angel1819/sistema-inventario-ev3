from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventario_home, name='inventario_home'),
    path('crear_producto/', views.crear_producto, name='crear_producto'),
]
