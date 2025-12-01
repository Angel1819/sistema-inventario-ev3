from django.shortcuts import render

# Create your views here.
def iniciar_sesion(request):
    return render(request, 'usuarios/iniciar_sesion.html')

def cerrar_sesion(request):
    return render(request, 'usuarios/cerrar_sesion.html')