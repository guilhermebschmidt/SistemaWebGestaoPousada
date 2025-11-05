import pytest
from datetime import date, timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from apps.core.models import Hospede, Quarto, Reserva
from apps.financeiro.models import Categoria, Titulo

# Pega o modelo de usuário do Django (necessário para testes de login)
User = get_user_model()

@pytest.fixture
def hospede(db):
    """Cria um hóspede válido para ser usado nos testes."""
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
    """Cria um quarto disponível para ser usado nos testes."""
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
    """Cria uma reserva válida para ser usada nos testes."""
    data_inicio = date.today() + timedelta(days=10)
    data_fim = data_inicio + timedelta(days=3)
    
    # Criamos a reserva sem salvar no banco ainda (commit=False)
    # para permitir que o método .save() seja testado
    reserva = Reserva(
        id_hospede=hospede,
        id_quarto=quarto,
        data_reserva_inicio=data_inicio,
        data_reserva_fim=data_fim
    )
    # O .save() aqui vai calcular valor e criar os títulos financeiros
    reserva.save() 
    return reserva

@pytest.fixture
def categoria_despesa(db):
    """Cria uma categoria de despesa."""
    return Categoria.objects.create(
        tipo='D',
        descricao="Limpeza"
    )

@pytest.fixture
def categoria_receita(db):
    """Cria uma categoria de receita."""
    return Categoria.objects.create(
        tipo='R',
        descricao="Receita de Hospedagem"
    )

@pytest.fixture
def titulo_receita(db, reserva):
    """Retorna o título de sinal (50%) criado automaticamente pela reserva."""
    # O .save() da reserva já criou os títulos.
    return Titulo.objects.get(
        reserva=reserva,
        descricao__startswith='Sinal'
    )

@pytest.fixture
def user(db):
    """Cria um usuário padrão para testes de login."""
    return User.objects.create_user(
        username='testuser', 
        email='user@test.com', 
        password='password123'
    )

@pytest.fixture
def auth_client(client, user):
    """Cria um cliente de teste que já está logado."""
    client.login(username='testuser', password='password123')
    return client