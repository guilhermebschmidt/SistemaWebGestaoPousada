from django.shortcuts import render, redirect, get_object_or_404
from ..models.reserva import Reserva
from ..forms.reserva import ReservaForm
from django.contrib import messages

def verifica_conflito_de_datas(quarto, data_inicio, data_fim, reserva_a_ignorar=None):
    """
        Função verifica se há conflito de datas para a reserva de um quarto e
        retorna a reserva conflitante se encontrar uma, ou None se estiver livre.
    """
    conflitos = Reserva.objects.filter(
        id_quarto=quarto,
        data_reserva_inicio__lt=data_fim,
        data_reserva_fim__gt=data_inicio
    ).exclude(status='CANCELADA')

    if reserva_a_ignorar:
        conflitos = conflitos.exclude(pk=reserva_a_ignorar.pk)
    
    return conflitos.first()

