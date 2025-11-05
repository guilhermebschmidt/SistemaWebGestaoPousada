import pytest
from django.db import IntegrityError
from apps.financeiro.models import Categoria, Titulo

def test_categoria_str(categoria_despesa, categoria_receita):
    assert str(categoria_despesa) == "Limpeza (Despesa)"
    assert str(categoria_receita) == "Receita de Hospedagem (Receita)"

def test_categoria_unique_together(db):
    """Testa se não é possível criar categorias com mesmo tipo e descrição."""
    Categoria.objects.create(tipo='D', descricao='Duplicada')
    with pytest.raises(IntegrityError):
        Categoria.objects.create(tipo='D', descricao='Duplicada')

def test_titulo_str(titulo_receita):
    assert str(titulo_receita) == f"{titulo_receita.descricao} - {titulo_receita.valor}"

<<<<<<< HEAD
    def test_categoria_creation_and_str(self):
        """Testa a criação e o método __str__ do modelo Categoria."""
        categoria_receita = Categoria.objects.create(tipo='R', descricao="Receita de Hospedagem")
        categoria_despesa = Categoria.objects.create(tipo='D', descricao="Despesa com Limpeza")
        assert Categoria.objects.count() == 2
        assert str(categoria_receita) == "Receita de Hospedagem (Receita)"
        assert str(categoria_despesa) == "Despesa com Limpeza (Despesa)"



@pytest.fixture
def setup_reserva(db):
    """Fixture para criar objetos relacionados para testar o Titulo."""
    hospede = Hospede.objects.create(
        cpf="12345678901", nome="João Teste", telefone="11987654321",
        email="joao@teste.com", data_nascimento="1990-01-01"
    )
    quarto = Quarto.objects.create(
        numero="101", tipo_quarto='SUITE', capacidade=2, preco=250.00
    )
    reserva = Reserva.objects.create(
        id_hospede=hospede, id_quarto=quarto, data_reserva_inicio=date.today(),
        data_reserva_fim=date.today(), valor=250.00
    )
    categoria = Categoria.objects.create(tipo='R', descricao="Teste")
    return hospede, reserva, categoria


@pytest.mark.django_db
def test_titulo_creation_with_reserva(setup_reserva):
    """Testa a criação de um Titulo associado a uma Reserva."""
    hospede, reserva, categoria = setup_reserva
    titulo = Titulo.objects.create(
        descricao="Pagamento da Reserva #1", valor=250.00, data=date.today(),
        data_vencimento=date.today(), tipo=True, cancelado=False, pago=False,
        reserva=reserva, hospede=hospede, categoria=categoria, tipo_documento='pix',
        conta_corrente='Principal'
    )
    assert Titulo.objects.count() == 1
    assert titulo.reserva == reserva
    assert titulo.hospede == hospede
    assert titulo.categoria == categoria
    # Formata dinamicamente para evitar discrepâncias de representação decimal
    assert str(titulo) == f"Pagamento da Reserva #1 - {titulo.valor:.2f}"


@pytest.mark.django_db
def test_titulo_tipo_display_method(setup_reserva):
    """Testa o método tipo_display do modelo Titulo."""
    hospede, reserva, categoria = setup_reserva
    titulo_entrada = Titulo.objects.create(
        descricao="Entrada", valor=100.00, data=date.today(), data_vencimento=date.today(),
        tipo=True, cancelado=False, pago=False, tipo_documento='pix', conta_corrente='Principal'
    )
    titulo_saida = Titulo.objects.create(
        descricao="Saída", valor=50.00, data=date.today(), data_vencimento=date.today(),
        tipo=False, cancelado=False, pago=False, tipo_documento='pix', conta_corrente='Principal'
    )
    assert titulo_entrada.tipo_display() == "Entrada"
    assert titulo_saida.tipo_display() == "Saída"
=======
def test_titulo_tipo_display(titulo_receita):
    titulo_receita.tipo = True # Entrada
    assert titulo_receita.tipo_display() == "Entrada"
    
    titulo_receita.tipo = False # Saída
    assert titulo_receita.tipo_display() == "Saída"
>>>>>>> 8b9ba418af16e0af05bb5b11558a927cfa1741f0
