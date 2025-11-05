import pytest
from datetime import date, timedelta
from apps.financeiro.forms import CategoriaDespesaForm, TituloForm

def test_categoria_despesa_form_valid(db):
    form = CategoriaDespesaForm(data={'descricao': 'Nova Categoria'})
    assert form.is_valid()

def test_titulo_form_valid(db, hospede, reserva, categoria_despesa):
    form_data = {
        'descricao': "Título de Teste",
        'valor': 100.00,
        'tipo_documento': 'pix',
        'conta_corrente': 'Conta Teste',
        'data': date.today().isoformat(),
        'data_vencimento': (date.today() + timedelta(days=5)).isoformat(),
        'hospede': hospede.id,
        'reserva': reserva.id,
        'categoria': categoria_despesa.id,
        'tipo': True, # Entrada
        'cancelado': False,
        'pago': False,
    }
    form = TituloForm(data=form_data)
    assert form.is_valid()

def test_titulo_form_campos_nao_obrigatorios(db):
    """Verifica se o form é válido sem hospede, reserva e categoria."""
    form_data = {
        'descricao': "Despesa Avulsa",
        'valor': 50.00,
        'tipo_documento': 'dinheiro',
        'conta_corrente': 'Caixa',
        'data': date.today().isoformat(),
        'data_vencimento': date.today().isoformat(),
        'tipo': False, # Saída
        'cancelado': False,
        'pago': True,
        'data_pagamento': date.today().isoformat(),
    }
    form = TituloForm(data=form_data)
    assert form.is_valid() # Deve ser válido
    assert form.cleaned_data['hospede'] is None
    assert form.cleaned_data['reserva'] is None
    assert form.cleaned_data['categoria'] is None