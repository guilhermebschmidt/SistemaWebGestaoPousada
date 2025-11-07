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

def form_quarto(request, pk=None, quarto_id=None):
    # aceitar tanto 'pk' quanto 'quarto_id' como identificador
    identifier = pk or quarto_id
    quarto = get_object_or_404(Quarto, pk=identifier) if identifier else None

    if request.method == 'POST':
        form = QuartoForm(request.POST, instance=quarto)
        if form.is_valid():
            form.save()
            msg = 'Quarto salvo com sucesso.'
            messages.success(request, msg)
            resp = redirect('quarto:listar')
            try:
                resp.set_cookie('messages', msg)
            except Exception:
                pass
            return resp
    else:
        form = QuartoForm(instance=quarto)
        print("Valores do formulário:")
        for field in form:
            print(f"{field.name}: {field.value()}")

    context = {
        'form': form,
        'quarto': quarto,
        'tipos_de_quarto': Quarto.TIPOS_QUARTOS_CHOICES,
        'is_editing':pk is not None,
        'debug_data': {
            'numero': quarto.numero if quarto else None,
            'preco': float(quarto.preco) if quarto and quarto.preco else None,
        } if quarto else None
    }
    return render(request, 'core/quarto/form.html', context)

def excluir(request, pk=None, quarto_id=None):
    identifier = pk or quarto_id
    quarto = get_object_or_404(Quarto, pk=identifier)
    
    if request.method == 'POST':
        quarto.delete()
        msg = f"O Quarto {quarto.numero} foi excluído com sucesso."
        messages.success(request, msg)
        resp = redirect('quarto:listar')
        try:
            resp.set_cookie('messages', msg)
        except Exception:
            pass
        return resp

    return redirect('quarto:listar')

def mudar_status_quarto(request, pk=None, quarto_id=None):
    identifier = pk or quarto_id
    quarto = get_object_or_404(Quarto, pk=identifier)

    if request.method == 'POST':
        form = QuartoStatusForm(request.POST, instance=quarto)
        if form.is_valid():
            form.save()
            msg = f"O status do Quarto {quarto.numero} foi atualizado com sucesso!"
            messages.success(request, msg)
            resp = redirect('quarto:listar')
            try:
                resp.set_cookie('messages', msg)
            except Exception:
                pass
            return resp
    else:
        form = QuartoStatusForm(instance=quarto)

    context = {
        'form': form,
        'quarto': quarto
    }
    return render(request, 'core/quarto/mudar_status.html', context)
