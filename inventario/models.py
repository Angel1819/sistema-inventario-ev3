from django.db import models

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre
    
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre de la empresa/proveedor
    nombre_contacto = models.CharField(max_length=100, blank=True)  # Persona de contacto (opcional)
    telefono_contacto = models.CharField(max_length=20, blank=True)  # Teléfono del contacto (opcional)
    email = models.EmailField(blank=True)  # Email del contacto o empresa
    direccion = models.CharField(max_length=200, blank=True)  # Dirección física (opcional)

    def __str__(self):
        return self.nombre

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