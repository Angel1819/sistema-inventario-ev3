from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'templates/catalogo_playa/base.html')