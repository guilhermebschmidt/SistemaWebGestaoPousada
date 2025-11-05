from django.shortcuts import render, redirect, get_object_or_404
from ..models.reserva import Reserva
from ..models.hospede import Hospede
from ..models.quarto import Quarto
from ..forms.reserva  import ReservaForm
from ..utils.emails import enviar_email_confirmacao
import datetime
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages


def list(request):
    filtro_status = request.GET.get('status', 'todos')
    filtro_hospede = request.GET.get('hospede', '')
    filtro_quarto = request.GET.get('quarto', 'todos')

    reservas = Reserva.objects.all().order_by('data_reserva_inicio')
    quartos = Quarto.objects.all()

    if filtro_status != 'todos':
        reservas = reservas.filter(status=filtro_status)

    if filtro_hospede:
        reservas = reservas.filter(id_hospede__nome__icontains=filtro_hospede)

    if filtro_quarto != 'todos':
        reservas = reservas.filter(id_quarto__id=filtro_quarto)


    context = {
        'reservas': reservas,
        'filtro_status': filtro_status,
        'filtro_hospede': filtro_hospede,
        'filtro_quarto': filtro_quarto,
        'quartos': quartos, 
    }

    return render(request, 'core/reserva/list.html', context)

def reserva_form(request, pk=None):
    if pk:
        instance = get_object_or_404(Reserva, pk=pk)
        success_message = "Reserva atualizada com sucesso!"
    else:
        instance = None
        success_message = "Reserva criada com sucesso!"

    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=instance)
        
        if form.is_valid():
            form.save()
            messages.success(request, success_message)
            return redirect('reserva:list')
        else:
            # Propagar erros não-field para o sistema de mensagens para
            # que templates que exibem mensagens possam mostrá-los aos testes.
            for err in form.non_field_errors():
                messages.error(request, str(err))
        
    else:
        # Se vierem parâmetros via GET (datas), repassa-los como initial para o form
        if request.GET.get('data_reserva_inicio') or request.GET.get('data_reserva_fim'):
            form = ReservaForm(initial=request.GET, instance=instance)
        else:
            form = ReservaForm(instance=instance)

    context = {
        'form': form,
        'reserva': instance
    }
    return render(request, 'core/reserva/form.html', context)


def search(request):
    query = request.GET.get('q', '')
    reservas = Reserva.objects.filter(id_hospede__nome__icontains=query)
    return render(request, 'core/reserva/list.html', {'reservas': reservas})

def list_checkin(request):
    hoje = datetime.date.today()
    reservas = Reserva.objects.filter(data_reserva_inicio = hoje)
    return render(request, 'core/reserva/list_check_in.html', {'reservas': reservas})

def list_checkout(request):
    hoje = datetime.date.today()
    reservas = Reserva.objects.filter(data_reserva_fim = hoje)
    return render(request, 'core/reserva/list_check_out.html', {'reservas': reservas})

def marcar_checkin(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    reserva.data_check_in = timezone.now()
    reserva.status = 'ATIVA'

    quarto = reserva.id_quarto
    quarto.status = 'OCUPADO'
    quarto.save()

    reserva.save()
    return redirect('reserva:list_checkin')

def marcar_checkout(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    reserva.data_check_out = timezone.now()
    reserva.status = 'CONCLUIDA'

    quarto = reserva.id_quarto
    quarto.status = 'DISPONIVEL'
    reserva.save()
    return redirect('reserva:list_checkout')

def cancelar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if reserva.status in ['CANCELADA', 'CONCLUIDA']:
        messages.error(request, f"A reserva #{pk} não pode ser cancelada, pois já está {reserva.status}.")
        return redirect('reserva:list')

    if reserva.data_check_in or reserva.data_check_out:
        messages.error(request, f"A reserva #{pk} já possui registro de Check-in/Check-out e não pode ser cancelada.")
        return redirect('reserva:list')
    if request.method != 'POST':
        return render(request, 'core/reserva/confirmar_cancelamento.html', {'reserva': reserva})

    motivo = request.POST.get('motivo_cancelamento', 'Motivo não especificado.')
    reserva.status = 'CANCELADA'
    reserva.motivo_cancelamento = motivo
    reserva.save()
    messages.success(request, f"A reserva #{pk} foi cancelada com sucesso.")
    return redirect('reserva:list')

def buscar_hospedes(request):
    if 'term' in request.GET:
        qs = Hospede.objects.filter(nome__icontains=request.GET.get('term'))
        hospedes = []
        for hospede in qs:
            hospedes.append({
                'id': hospede.id,
                'label': hospede.nome,
                'value': hospede.nome
            })
        return JsonResponse(hospedes, safe=False)
    return JsonResponse([], safe=False)

def enviar_confirmacao_email_view(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)

    if request.method == 'POST':
        try:
            enviar_email_confirmacao(reserva)
            reserva.email_confirmacao_enviado = True
            reserva.save()
            messages.success(request, f"E-mail de confirmação enviado com sucesso para {reserva.hospede.email}.")
        except Exception as e:
            print(f"DEBUG: O erro ao enviar o e-mail foi: {e}")
            messages.error(request, f"Ocorreu um erro ao enviar o e-mail: {e}")

    return redirect('reserva:list')

