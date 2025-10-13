from django.shortcuts import render, redirect, get_object_or_404
from ..models.quarto import Quarto
from ..forms.quarto import QuartoForm, QuartoStatusForm 
from django.contrib import messages

def index(request):
    return render(request, 'core/quarto/index.html')#, {'quartos': list})

def listar(request):
    filtro_tipo = request.GET.get('tipo_quarto', 'todos')
    quartos = Quarto.objects.all().order_by('numero')

    if filtro_tipo != 'todos':
        quartos = quartos.filter(tipo_quarto=filtro_tipo)

    context = {
        'quartos': quartos,
        'tipos_de_quarto': Quarto.TIPOS_QUARTOS_CHOICES,
        'filtro_tipo_atual': filtro_tipo,
    }
    return render(request, 'core/quarto/listar.html', context)

def form(request, quarto_id=None):
    quarto = get_object_or_404(Quarto, pk=quarto_id) if quarto_id else None

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
        'tipos_de_quarto': Quarto.TIPOS_QUARTOS_CHOICES,
        'is_editing': quarto_id is not None,
        'debug_data': {
            'numero': quarto.numero if quarto else None,
            'preco': float(quarto.preco) if quarto and quarto.preco else None,
        } if quarto else None
    }
    return render(request, 'core/quarto/form.html', context)

def tipos_quarto(request):
    return render(request, 'core/quarto/tipos_quarto.html')

def excluir(request, quarto_id):
    quarto = get_object_or_404(Quarto, pk=quarto_id)
    if request.method == 'POST':
        quarto.delete()
        return redirect('core/quarto:list')
    return render(request, 'core/quarto/listar.html', {'quarto': quarto})

def mudar_status_quarto(request, pk):
    quarto = get_object_or_404(Quarto, pk=pk)

    if request.method == 'POST':
        form = QuartoStatusForm(request.POST, instance=quarto)
        if form.is_valid():
            form.save()
            messages.success(request, f"O status do Quarto {quarto.numero} foi atualizado com sucesso!")
            return redirect('quarto:listar')
    else:
        form = QuartoStatusForm(instance=quarto)

    context = {
        'form': form,
        'quarto': quarto
    }
    return render(request, 'core/quarto/mudar_status.html', context)
