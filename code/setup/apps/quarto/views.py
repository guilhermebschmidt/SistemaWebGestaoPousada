from django.shortcuts import render, redirect
from .models import Quarto
from .forms import QuartoForm

def index(request):
    return render(request, 'quarto/index.html')

def quartos(request):
    quartos = Quarto.objects.all()
    return render(request, 'quarto/quartos.html', {'quartos': quartos})

def adicionar_quarto(request):
    if request.method == 'POST':
        form = QuartoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quarto:quartos')
    else:
        form = QuartoForm()
    return render(request, 'quarto/adicionar_quarto.html', {'form': form})

def tipos_quarto(request):
    return render(request, 'quarto/tipos_quarto.html')
