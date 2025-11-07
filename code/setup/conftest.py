import pytest
from datetime import date, timedelta
from django.contrib.auth import get_user_model
from apps.core.models import Hospede, Quarto, Reserva
from apps.financeiro.models import Categoria, Titulo


User = get_user_model()


@pytest.fixture
def hospede(db):
    return Hospede.objects.create(
        cpf="12345678901",
        nome="Hóspede Teste",
        telefone="11999998888",
        email="hospede.teste@email.com",
        data_nascimento=date(1990, 1, 1),
        rua="Rua Teste",
        numero="123",
        bairro="Bairro Teste",
        cidade="Cidade Teste",
        cep="12345678"
    )


@pytest.fixture
def quarto(db):
    return Quarto.objects.create(
        numero="101",
        status='DISPONIVEL',
        tipo_quarto='SUITE',
        descricao="Quarto de teste",
        capacidade=2,
        preco=200.00
    )


@pytest.fixture
def reserva(db, hospede, quarto):
    data_inicio = date.today() + timedelta(days=10)
    data_fim = data_inicio + timedelta(days=3)
    reserva = Reserva(
        id_hospede=hospede,
        id_quarto=quarto,
        data_reserva_inicio=data_inicio,
        data_reserva_fim=data_fim
    )
    reserva.save()
    return reserva


@pytest.fixture
def categoria_despesa(db):
    return Categoria.objects.create(tipo='D', descricao='Limpeza')


@pytest.fixture
def categoria_receita(db):
    return Categoria.objects.create(tipo='R', descricao='Receita de Hospedagem')


@pytest.fixture
def titulo_receita(db, reserva):
    return Titulo.objects.get(reserva=reserva, descricao__startswith='Sinal')


@pytest.fixture
def titulo_receita_sinal(db, reserva):
    """Compatibilidade com fixtures usadas em apps/financeiro/tests."""
    return Titulo.objects.get(reserva=reserva, descricao__startswith='Sinal')


@pytest.fixture
def titulo_receita_restante(db, reserva):
    """Compatibilidade: retorna o título restante criado pela reserva."""
    return Titulo.objects.get(reserva=reserva, descricao__startswith='Pagamento Restante')
