from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .decorators import rol_requerido, solo_administrador
from .models import Usuario
from .forms import LoginForm


# ═══════════════════════════════════════════════════════════════
# LOGIN
# ═══════════════════════════════════════════════════════════════

def iniciar_sesion(request):
    # Si ya está logueado, lo manda al inventario
    if request.user.is_authenticated:
        return redirect('inventario_home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            # El formulario ya validó las credenciales
            # El usuario autenticado está en form.user
            login(request, form.user)
            return redirect('home')
        # Si no es válido, el formulario tendrá los errores
    else:
        form = LoginForm()
    
    return render(request, 'usuarios/iniciar_sesion.html', {
        'form': form
    })


# ═══════════════════════════════════════════════════════════════
# LOGOUT
# ═══════════════════════════════════════════════════════════════

@login_required(login_url='iniciar_sesion')
def cerrar_sesion(request):
    # Destruir la sesión
    logout(request)
    # Redirigir al login
    return redirect('iniciar_sesion')
