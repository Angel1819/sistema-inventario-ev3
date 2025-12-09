from functools import wraps  # ← Para crear decoradores
from django.contrib.auth.decorators import login_required  # ← Verifica si estás logueado
from django.http import HttpResponseForbidden  # ← Mensaje de "no tienes permiso"
from .models import Usuario  # ← Importar nuestro modelo Usuario

# ═══════════════════════════════════════════════════════════════
# DECORADOR PARA VERIFICAR ROL
# ═══════════════════════════════════════════════════════════════

def rol_requerido(*roles_permitidos):
    # roles_permitidos es una lista de roles que pueden acceder
    # Ejemplo: @rol_requerido('administrador') o @rol_requerido('administrador', 'vendedor')
    
    def decorador(view_func):
        # view_func es la vista que quieres proteger
        
        @wraps(view_func)  # ← Mantiene el nombre original de la función
        @login_required(login_url='login')  # ← PRIMERO verifica que esté logueado
        # Si no está logueado, lo manda a la página 'login'
        def wrapper(request, *args, **kwargs):
            # request contiene información del usuario actual
            
            try:
                # Intenta obtener el Usuario del usuario logueado
                usuario = request.user.usuario
                # request.user es el User de Django
                # .usuario es nuestro modelo Usuario conectado
                
                # Verificar si el rol del usuario está en los roles permitidos
                if usuario.rol in roles_permitidos:
                    # ✅ Tiene permiso, ejecuta la vista normalmente
                    return view_func(request, *args, **kwargs)
                else:
                    # ❌ NO tiene permiso, muestra error 403
                    return HttpResponseForbidden(
                        f"No tienes permiso. Roles requeridos: {roles_permitidos}"
                    )
                    
            except Usuario.DoesNotExist:
                # Si no existe un Usuario para este User
                return HttpResponseForbidden("Usuario no encontrado")
        
        return wrapper
    return decorador

# ═══════════════════════════════════════════════════════════════
# DECORADOR SIMPLIFICADO SOLO PARA ADMIN
# ═══════════════════════════════════════════════════════════════

def solo_administrador(view_func):
    # Es lo mismo que @rol_requerido('administrador') pero más corto
    
    @wraps(view_func)
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        try:
            # Obtener el Usuario
            usuario = request.user.usuario
            
            # Verificar si es administrador
            if usuario.rol == 'administrador':
                # ✅ Es admin, ejecutar la vista
                return view_func(request, *args, **kwargs)
            else:
                # ❌ No es admin
                return HttpResponseForbidden("Solo administradores pueden acceder")
                
        except Usuario.DoesNotExist:
            return HttpResponseForbidden("Usuario no encontrado")
    
    return wrapper
