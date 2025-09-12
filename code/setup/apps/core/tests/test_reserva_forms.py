import pytest
import datetime
from apps.core.forms.reserva import ReservaForm
from apps.core.models.hospede import Hospede
from apps.core.models.quarto import Quarto
from apps.core.models.reserva import Reserva

@pytest.mark.django_db
def test_reserva_form_valid():
    """Testa ReservaForm com dados válidos"""
    # Criando objetos necessários
    hospede = Hospede.objects.create(nome="João", cpf="12345678901", data_nascimento="1990-01-01", telefone="999999999", email="joao@email.com")
    quarto = Quarto.objects.create(numero="101", status=True, descricao="Quarto confortável", preco=200.0)

    data = {
        'id_hospede': hospede.id,
        'id_quarto': quarto.id,
        'data_reserva_inicio': datetime.date.today(),
        'data_reserva_fim': datetime.date.today() + datetime.timedelta(days=2),
    }

    form = ReservaForm(data=data)
    assert form.is_valid(), form.errors
    reserva = form.save(commit=False)
    assert reserva.id_hospede == hospede
    assert reserva.id_quarto == quarto
    assert reserva.data_reserva_inicio == datetime.date.today()
    assert reserva.data_reserva_fim == datetime.date.today() + datetime.timedelta(days=2)

@pytest.mark.django_db
def test_reserva_form_invalid_past_start():
    """Testa ReservaForm com data de início no passado"""
    hospede = Hospede.objects.create(nome="João", cpf="12345678901", data_nascimento="1990-01-01", telefone="999999999", email="joao@email.com")
    quarto = Quarto.objects.create(numero="101", status=True, descricao="Quarto confortável", preco=200.0)

    data = {
        'id_hospede': hospede.id,
        'id_quarto': quarto.id,
        'data_reserva_inicio': datetime.date.today() - datetime.timedelta(days=1),
        'data_reserva_fim': datetime.date.today() + datetime.timedelta(days=2),
    }

    form = ReservaForm(data=data)
    assert not form.is_valid()
    assert 'data_reserva_inicio' in form.errors

@pytest.mark.django_db
def test_reserva_form_invalid_end_before_start():
    """Testa ReservaForm com data de fim antes da data de início"""
    hospede = Hospede.objects.create(nome="João", cpf="12345678901", data_nascimento="1990-01-01", telefone="999999999", email="joao@email.com")
    quarto = Quarto.objects.create(numero="101", status=True, descricao="Quarto confortável", preco=200.0)

    data = {
        'id_hospede': hospede.id,
        'id_quarto': quarto.id,
        'data_reserva_inicio': datetime.date.today() + datetime.timedelta(days=1),
        'data_reserva_fim': datetime.date.today(),
    }

    form = ReservaForm(data=data)
    assert not form.is_valid()
    assert 'data_reserva_fim' in form.errors

@pytest.mark.django_db
def test_reserva_form_missing_fields():
    """Testa se o form detecta campos obrigatórios ausentes"""
    form = ReservaForm(data={})
    assert not form.is_valid()
    required_fields = ['id_hospede', 'id_quarto', 'data_reserva_inicio', 'data_reserva_fim']
    for field in required_fields:
        assert field in form.errors
