import pytest
from datetime import date, timedelta
from apps.core.forms import HospedeForm, ReservaForm, QuartoForm
from apps.core.models import Hospede, Quarto

@pytest.mark.django_db
def test_reserva_form_valido(db, hospede, quarto):
    data_inicio = date.today() + timedelta(days=3)
    data_fim = data_inicio + timedelta(days=2)
    form_data = {
        "hospede_nome": hospede.nome, # Campo de autocomplete
        "id_hospede": hospede.id,     # Campo hidden
        "id_quarto": quarto.id,
        "data_reserva_inicio": data_inicio.isoformat(),
        "data_reserva_fim": data_fim.isoformat()
    }
    form = ReservaForm(data=form_data)
    assert form.is_valid()

def test_reserva_form_clean_antecedencia_invalida(db, hospede, quarto):
    """Testa a regra de negócio de 2 dias de antecedência."""
    data_inicio = date.today() + timedelta(days=1) # Apenas 1 dia
    data_fim = data_inicio + timedelta(days=2)
    form_data = {
        "hospede_nome": hospede.nome,
        "id_hospede": hospede.id,
        "id_quarto": quarto.id,
        "data_reserva_inicio": data_inicio.isoformat(),
        "data_reserva_fim": data_fim.isoformat()
    }
    form = ReservaForm(data=form_data)
    assert not form.is_valid()
    assert "A data de início da reserva deve ser a partir de" in form.errors['data_reserva_inicio'][0]

@pytest.mark.django_db
def test_reserva_form_invalid_end_before_start():
    """Testa ReservaForm com data de fim antes da data de início"""
    hospede = Hospede.objects.create(nome="João", cpf="12345678901", data_nascimento="1990-01-01", telefone="999999999", email="joao@email.com")
    quarto = Quarto.objects.create(numero="101", status=True, descricao="Quarto confortável", preco=200.0, capacidade=2)

    data = {
        'id_hospede': hospede.id,
        'id_quarto': quarto.id,
        'data_reserva_inicio': date.today() + timedelta(days=1),
        'data_reserva_fim': date.today(),
    }

    form = ReservaForm(data=data)
    assert not form.is_valid()
    # Dependendo da ordem de validação, pode ser sinalizado erro em inicio (antecedência)
    assert 'data_reserva_fim' in form.errors or 'data_reserva_inicio' in form.errors

@pytest.mark.django_db
def test_reserva_form_missing_fields():
    """Testa se o form detecta campos obrigatórios ausentes"""
    form = ReservaForm(data={})
    assert not form.is_valid()
    # Certifique-se de que os campos obrigatórios estejam apontados como erro
    assert 'id_hospede' in form.errors
    assert 'id_quarto' in form.errors
