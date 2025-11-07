import pytest
from datetime import date, timedelta
from apps.core.forms import ReservaForm
from apps.core.models import Hospede, Quarto

@pytest.mark.django_db
def test_reserva_form_valid(db, hospede, quarto):
    data_inicio = date.today() + timedelta(days=3)
    data_fim = data_inicio + timedelta(days=2)
    form_data = {
        "hospede_nome": hospede.nome, "id_hospede": hospede.id,
        "id_quarto": quarto.id,
        "data_reserva_inicio": data_inicio.isoformat(),
        "data_reserva_fim": data_fim.isoformat(),
        "quantidade_adultos": 2, "quantidade_criancas": 0
    }
    form = ReservaForm(data=form_data)
    assert form.is_valid(), form.errors

@pytest.mark.django_db
def test_reserva_form_erro_excesso_capacidade(db, hospede, quarto):
    data_inicio = date.today() + timedelta(days=3)
    data_fim = data_inicio + timedelta(days=2)
    form_data = {
        "hospede_nome": hospede.nome, "id_hospede": hospede.id,
        "id_quarto": quarto.id, # quarto da fixture tem capacidade 2
        "data_reserva_inicio": data_inicio.isoformat(),
        "data_reserva_fim": data_fim.isoformat(),
        "quantidade_adultos": 2, "quantidade_criancas": 1 # Total 3 pessoas
    }
    form = ReservaForm(data=form_data)
    assert not form.is_valid()
    assert "excede a capacidade do quarto (2)" in form.non_field_errors()[0]

@pytest.mark.django_db
def test_reserva_form_erro_zero_pessoas(db, hospede, quarto):
    data_inicio = date.today() + timedelta(days=3)
    data_fim = data_inicio + timedelta(days=2)
    form_data = {
        "hospede_nome": hospede.nome, "id_hospede": hospede.id,
        "id_quarto": quarto.id,
        "data_reserva_inicio": data_inicio.isoformat(),
        "data_reserva_fim": data_fim.isoformat(),
        "quantidade_adultos": 0, "quantidade_criancas": 0
    }
    form = ReservaForm(data=form_data)
    assert not form.is_valid()
    assert "A reserva deve ser para pelo menos 1 pessoa." in form.errors['quantidade_adultos']

@pytest.mark.django_db
def test_reserva_form_clean_antecedencia_invalida(db, hospede, quarto):
    data_inicio = date.today() + timedelta(days=1) # Apenas 1 dia
    form = ReservaForm(data={'data_reserva_inicio': data_inicio.isoformat()})
    assert not form.is_valid()
    assert "A data de início da reserva deve ser a partir de" in form.errors['data_reserva_inicio'][0]

@pytest.mark.django_db
def test_reserva_form_clean_data_fim_invalida(db, hospede, quarto):
    data_inicio = date.today() + timedelta(days=3)
    data_fim = data_inicio # Fim igual ao início
    form = ReservaForm(data={
        'data_reserva_inicio': data_inicio.isoformat(),
        'data_reserva_fim': data_fim.isoformat()
    })
    assert not form.is_valid()
    assert "A data de fim deve ser posterior à data de início." in form.errors['data_reserva_fim']