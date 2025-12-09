from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .decorators import rol_requerido, solo_administrador
from .models import Usuario


# ═══════════════════════════════════════════════════════════════
# LOGIN
# ═══════════════════════════════════════════════════════════════

def iniciar_sesion(request):
    # Si ya está logueado, lo manda al inventario
    if request.user.is_authenticated:
        return redirect('inventario_home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Buscar usuario con esas credenciales
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # ✅ Credenciales correctas
            login(request, user)  # Crear sesión
            return redirect('inventario_home')
        else:
            # ❌ Credenciales incorrectas
            return render(request, 'usuarios/iniciar_sesion.html', {
                'error': 'Usuario o contraseña incorrectos'
            })
    
    return render(request, 'usuarios/iniciar_sesion.html')


# ═══════════════════════════════════════════════════════════════
# LOGOUT
# ═══════════════════════════════════════════════════════════════

@login_required(login_url='iniciar_sesion')
def cerrar_sesion(request):
    # Destruir la sesión
    logout(request)
    # Redirigir al login
    return redirect('iniciar_sesion')
