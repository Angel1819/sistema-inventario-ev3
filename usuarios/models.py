from django.db import models
from django.contrib.auth.models import User  # ← Importar el User de Django (importante)

class Usuario(models.Model):
    # Definir los roles disponibles
    class Rol(models.TextChoices):
        ADMINISTRADOR = 'administrador', 'Administrador'  # Valor en BD, Valor visible
        VENDEDOR = 'vendedor', 'Vendedor'
    
    # Conectar con User de Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Explicación: Cada Usuario tiene UN User de Django (relación 1 a 1)
    # on_delete=CASCADE significa: si borras el User, también se borra el Usuario
    
    # Campo de rol
    rol = models.CharField(
        max_length=50,
        choices=Rol.choices,
        default=Rol.VENDEDOR
    )
    # Explicación: Aquí guardamos si es 'administrador' o 'vendedor'
    
    # Campos adicionales
    telefono = models.CharField(max_length=20, blank=True)  # Teléfono

    def __str__(self):
        return f"{self.user.username} - {self.get_rol_display()}"
