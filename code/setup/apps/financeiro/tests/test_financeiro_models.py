import pytest
from datetime import date
from apps.financeiro.models import Banco, Categoria, Titulo
from apps.core.models import Hospede, Quarto, Reserva

@pytest.mark.django_db
class TestFinanceiroModels:

    def test_banco_creation_and_str(self):
        """Testa a criação e o método __str__ do modelo Banco.

        Usa get_or_create para evitar UniqueViolation caso existam seeds no DB de teste.
        """
        banco, created = Banco.objects.get_or_create(codigo="260", defaults={
            'descricao': "Nu Pagamentos S.A. (Nubank)"
        })
        assert Banco.objects.filter(codigo=banco.codigo).exists()
        assert str(banco) == f"{banco.codigo} - {banco.descricao}"
        assert banco._meta.db_table == "financeiro_banco"

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

    def test_titulo_creation_with_reserva(self, setup_reserva):
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

    def test_titulo_tipo_display_method(self, setup_reserva):
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