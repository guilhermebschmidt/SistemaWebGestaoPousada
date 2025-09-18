from django.shortcuts import render, redirect, get_object_or_404
from ..models.quarto import Quarto
from ..forms.quarto import QuartoForm
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'core/quarto/index.html', {'quartoss': quartos})

@login_required
def quartos(request):
    quartos = Quarto.objects.all()
    return render(request, 'core/quarto/quartos.html', {'quartos': quartos})

@login_required
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
            return redirect('/quartos/')
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
    return render(request, 'core/quarto/form.html', context)

@login_required
def tipos_quarto(request):
    return render(request, 'core/quarto/tipos_quarto.html')

@login_required
def excluir_quarto(request, quarto_id):
    quarto = get_object_or_404(Quarto, pk=quarto_id)
    if request.method == 'POST':
        quarto.delete()
        return redirect('core/quarto:quartos')
    return render(request, 'core/quarto/excluir_quarto.html', {'quarto': quarto})