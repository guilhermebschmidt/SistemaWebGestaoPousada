from django.shortcuts import render
from .models import Quarto


def index(request):
    return render(request, 'quarto/index.html')

def quartos(request):
    quartos = Quarto.objects.all()
    return render(request, 'quarto/quartos.html', {'quartos':quartos})