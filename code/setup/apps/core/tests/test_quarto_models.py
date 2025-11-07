import pytest
from apps.core.models import Quarto, Reserva
from datetime import date, timedelta


@pytest.mark.django_db
def test_create_quarto(db):
    quarto = Quarto.objects.create(
        numero="101", status='DISPONIVEL', descricao="Quarto com vista",
        preco=250.75, capacidade=2, tipo_quarto='SUITE'
    )
    saved_quarto = Quarto.objects.get(numero="101")
    assert saved_quarto.status == 'DISPONIVEL'
    assert saved_quarto.descricao == "Quarto com vista"

@pytest.mark.django_db
def test_quarto_str_method(quarto):
    assert str(quarto) == "Quarto 101"

@pytest.mark.django_db
def test_quarto_fields_properties(db):
    field_numero = Quarto._meta.get_field('numero')
    assert field_numero.max_length == 100


@pytest.mark.django_db
def test_quarto_is_available_livre(quarto):
    data_inicio = date.today() + timedelta(days=5)
    data_fim = data_inicio + timedelta(days=3)
    assert quarto.is_available(data_inicio, data_fim) is True

@pytest.mark.django_db
def test_quarto_is_available_conflito_confirmada(db, hospede, quarto):
    # Cria uma reserva CONFIRMADA no período
    Reserva.objects.create(
        id_hospede=hospede, id_quarto=quarto, status='CONFIRMADA',
        data_reserva_inicio = date.today() + timedelta(days=5),
        data_reserva_fim = date.today() + timedelta(days=8)
    )
    # Tenta reservar sobrepondo
    data_inicio_conflito = date.today() + timedelta(days=6)
    data_fim_conflito = date.today() + timedelta(days=7)
    assert quarto.is_available(data_inicio_conflito, data_fim_conflito) is False

@pytest.mark.django_db
def test_quarto_is_available_ignora_reserva_cancelada(db, hospede, quarto):
    # Cria uma reserva CANCELADA no período
    Reserva.objects.create(
        id_hospede=hospede, id_quarto=quarto, status='CANCELADA',
        data_reserva_inicio = date.today() + timedelta(days=5),
        data_reserva_fim = date.today() + timedelta(days=8)
    )
    # Tenta reservar sobrepondo (deve ignorar a cancelada)
    data_inicio_conflito = date.today() + timedelta(days=6)
    data_fim_conflito = date.today() + timedelta(days=7)
    assert quarto.is_available(data_inicio_conflito, data_fim_conflito) is True

@pytest.mark.django_db
def test_quarto_is_available_ignora_reserva_atual(reserva, quarto):
    assert quarto.is_available(
        reserva.data_reserva_inicio, 
        reserva.data_reserva_fim, 
        reserva_a_ignorar=reserva
    ) is True