import pytest
from datetime import date, timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from apps.core.models import Hospede, Quarto, Reserva, Mensalista
from apps.financeiro.models import Categoria, Titulo

# Pega o modelo de usuário do Django (necessário para testes de login)
User = get_user_model()

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

@pytest.fixture
def hospede(db):
    """Cria um hóspede válido (com CPF) para ser usado nos testes."""
    return Hospede.objects.create(
        cpf="12345678901",
        nome="Hóspede Teste CPF",
        telefone="11999998888",
        email="hospede.teste@email.com",
        data_nascimento=date(1990, 1, 1),
        rua="Rua Teste", numero="123", bairro="Bairro Teste",
        cidade="Cidade Teste", cep="12345678"
    )

@pytest.fixture
def hospede_passaporte(db):
    """Cria um hóspede válido (com Passaporte) para ser usado nos testes."""
    return Hospede.objects.create(
        passaporte="ABC123456",
        nome="Hóspede Teste Passaporte",
        telefone="11999997777",
        email="hospede.passaporte@email.com",
        data_nascimento=date(1990, 1, 1),
        rua="Rua Teste", numero="123", bairro="Bairro Teste",
        cidade="Cidade Teste", cep="12345678"
    )

@pytest.fixture
def quarto(db):
    """Cria um quarto disponível (capacidade 2) para ser usado nos testes."""
    return Quarto.objects.create(
        numero="101",
        status='DISPONIVEL',
        tipo_quarto='SUITE',
        descricao="Quarto de teste",
        capacidade=2, # Capacidade 2
        preco=200.00
    )

@pytest.fixture
def quarto_grande(db):
    """Cria um quarto disponível (capacidade 4) para ser usado nos testes."""
    return Quarto.objects.create(
        numero="102",
        status='DISPONIVEL',
        tipo_quarto='LOFT',
        descricao="Quarto grande",
        capacidade=4, # Capacidade 4
        preco=300.00
    )

@pytest.fixture
def reserva(db, hospede, quarto):
    """
    Cria uma reserva (PREVISTA) no futuro (2 adultos, 0 crianças).
    O .save() desta reserva JÁ CRIA os títulos financeiros.
    """
    data_inicio = date.today() + timedelta(days=10)
    data_fim = data_inicio + timedelta(days=3)
    
    reserva = Reserva(
        id_hospede=hospede,
        id_quarto=quarto,
        data_reserva_inicio=data_inicio,
        data_reserva_fim=data_fim,
        quantidade_adultos=2,
        quantidade_criancas=0
    )
    reserva.save() 
    return reserva

@pytest.fixture
def mensalista(db, hospede, quarto):
    """Cria um mensalista ativo."""
    return Mensalista.objects.create(
        hospede=hospede,
        quarto=quarto,
        valor_mensal=1500.00,
        dia_vencimento=10,
        data_inicio=date.today(),
        ativo=True
    )

@pytest.fixture
def categoria_despesa(db):
    """Cria uma categoria de despesa (Tipo D)."""
    return Categoria.objects.create(
        tipo='D',
        descricao="Limpeza"
    )

@pytest.fixture
def categoria_receita(db):
    """Cria uma categoria de receita (Tipo R)."""
    return Categoria.objects.create(
        tipo='R',
        descricao="Receita de Hospedagem"
    )

@pytest.fixture
def titulo_receita_sinal(db, reserva):
    """Retorna o título de sinal (50%) criado automaticamente pela reserva."""
    return Titulo.objects.get(
        reserva=reserva,
        descricao__startswith='Sinal'
    )
    
@pytest.fixture
def titulo_receita_restante(db, reserva):
    """Retorna o título restante (50%) criado automaticamente pela reserva."""
    return Titulo.objects.get(
        reserva=reserva,
        descricao__startswith='Pagamento Restante'
    )