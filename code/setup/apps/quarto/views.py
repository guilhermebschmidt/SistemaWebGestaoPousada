from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Quarto
from .forms import QuartoForm

def index(request):
    return render(request, 'quarto/index.html')

def quartos(request):
    quartos = Quarto.objects.all()
    return render(request, 'quarto/quartos.html', {'quartos': quartos})

def form(request, quarto_id=None):
    quarto = get_object_or_404(Quarto, pk=quarto_id) if quarto_id else None

    if quarto:
        print(f"Valores do quarto (ID: {quarto.id}):")
        print(f"Número: {quarto.numero}")
        print(f"Preço: {quarto.preco}")
        print(f"Status: {quarto.status}")
        print(f"Descrição: {quarto.descricao}")

    if request.method == 'POST':
        form = QuartoForm(request.POST, instance=quarto)
        if form.is_valid():
            form.save()
            return redirect('quarto:quartos')
    else:
        form = QuartoForm(instance=quarto)
        print("Valores do formulário:")
        for field in form:
            print(f"{field.name}: {field.value()}")

    context = {
        'form': form,
        'quarto': quarto,
        'is_editing': quarto_id is not None,
        'debug_data': {
            'numero': quarto.numero if quarto else None,
            'preco': float(quarto.preco) if quarto and quarto.preco else None,
        } if quarto else None
    }
    return render(request, 'quarto/form.html', context)

def tipos_quarto(request):
    return render(request, 'quarto/tipos_quarto.html')

def excluir_quarto(request, quarto_id):
    quarto = get_object_or_404(Quarto, pk=quarto_id)
    if request.method == 'POST':
        quarto.delete()
        return redirect('quarto:quartos')
    return render(request, 'quarto/excluir_quarto.html', {'quarto': quarto})