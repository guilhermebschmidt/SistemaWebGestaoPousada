import pytest
from datetime import date
from apps.financeiro.forms import CategoriaDespesaForm, TituloForm
from apps.core.models import Hospede, Quarto, Reserva
from apps.financeiro.models import Categoria

@pytest.mark.django_db
class TestFinanceiroForms:

    def test_categoria_despesa_form_valid(self):
        """Testa o CategoriaDespesaForm com dados válidos."""
        form_data = {'descricao': 'Manutenção'}
        form = CategoriaDespesaForm(data=form_data)
        assert form.is_valid()

    def test_categoria_despesa_form_invalid(self):
        """Testa o CategoriaDespesaForm com dados inválidos (descrição vazia)."""
        form_data = {'descricao': ''}
        form = CategoriaDespesaForm(data=form_data)
        assert not form.is_valid()
        assert 'descricao' in form.errors

    @pytest.fixture
    def setup_relations(self):
        """Fixture para criar objetos relacionados para o TituloForm."""
        hospede = Hospede.objects.create(
            cpf="11122233344", nome="Maria Form", telefone="11987654321",
            email="maria@form.com", data_nascimento="1992-02-02"
        )
        quarto = Quarto.objects.create(numero="202", tipo_quarto='LOFT', capacidade=4, preco=400.00)
        reserva = Reserva.objects.create(
            id_hospede=hospede, id_quarto=quarto, data_reserva_inicio=date.today(),
            data_reserva_fim=date.today(), valor=400.00
        )
        categoria = Categoria.objects.create(tipo='R', descricao="Form Test")
        return hospede, reserva, categoria

    def test_titulo_form_valid(self, setup_relations):
        """Testa o TituloForm com dados válidos."""
        hospede, reserva, categoria = setup_relations
        form_data = {
            'descricao': 'Pagamento de teste',
            'valor': 150.75,
            'tipo_documento': 'pix',
            'conta_corrente': 'Conta Teste',
            'data': date.today().isoformat(),
            'data_vencimento': date.today().isoformat(),
            'hospede': hospede.pk,
            'reserva': reserva.pk,
            'categoria': categoria.pk,
            'tipo': 'True',  # Simula o valor de um RadioSelect
            'cancelado': 'False',
            'pago': 'False',
        }
        form = TituloForm(data=form_data)
        assert form.is_valid(), form.errors

    def test_titulo_form_missing_required_fields(self):
        """Testa o TituloForm sem dados obrigatórios."""
        form = TituloForm(data={})
        assert not form.is_valid()
        assert 'descricao' in form.errors
        assert 'valor' in form.errors
        assert 'data' in form.errors
        assert 'data_vencimento' in form.errors

    def test_titulo_form_optional_fields(self):
        """Testa se o TituloForm é válido sem os campos opcionais (hospede, reserva, categoria)."""
        form_data = {
            'descricao': 'Despesa Avulsa',
            'valor': 50.00,
            'tipo_documento': 'dinheiro',
            'conta_corrente': 'Caixa',
            'data': date.today().isoformat(),
            'data_vencimento': date.today().isoformat(),
            'tipo': 'False',
            'cancelado': 'False',
            'pago': 'True',
            'data_pagamento': date.today().isoformat(),
        }
        form = TituloForm(data=form_data)
        assert form.is_valid(), form.errors