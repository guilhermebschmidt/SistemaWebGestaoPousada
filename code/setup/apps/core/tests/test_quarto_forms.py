# apps/quarto/tests/test_forms.py
import pytest
from datetime import date, timedelta
from apps.core.forms import HospedeForm, ReservaForm, QuartoForm

@pytest.mark.django_db
def test_quarto_form_valido(db):
    form_data = {
        "numero": "102",
        "capacidade": 2,
        "tipo_quarto": "SUITE",
        "descricao": "Teste",
        "preco": 250.00
    }
    form = QuartoForm(data=form_data)
    assert form.is_valid()

@pytest.mark.django_db
def test_quarto_form_invalid_data():
    """Testa se o QuartoForm detecta dados inválidos"""
    data = {
        'numero': '',  # Campo obrigatório vazio
        # status é campo com choices (string) no model; aqui omitimos capacidade e descricao
        'descricao': '',  # Campo obrigatório vazio
        'preco': -50  # Valor negativo, se tiver validação
    }
    form = QuartoForm(data=data)
    assert not form.is_valid()  # Deve ser inválido
    # Verifica se os erros existem
    assert 'numero' in form.errors
    assert 'descricao' in form.errors
    # Capacidade é obrigatória no model
    assert 'capacidade' in form.errors
