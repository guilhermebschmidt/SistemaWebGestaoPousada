from django.shortcuts import render, redirect, get_object_or_404
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

def editar_quarto(request, quarto_id):
    quarto = get_object_or_404(Quarto, pk=quarto_id)
    if request.method == 'POST':
        form = QuartoForm(request.POST, instance=quarto)
        if form.is_valid():
            form.save()
            return redirect('quarto:quartos')
    else:
        form = QuartoForm(instance=quarto)
    return render(request, 'quarto/editar_quarto.html', {'form': form, 'quarto': quarto})

def excluir_quarto(request, quarto_id):
    quarto = get_object_or_404(Quarto, pk=quarto_id)
    if request.method == 'POST':
        quarto.delete()
        return redirect('quarto:quartos')
    return render(request, 'quarto/excluir_quarto.html', {'quarto': quarto})