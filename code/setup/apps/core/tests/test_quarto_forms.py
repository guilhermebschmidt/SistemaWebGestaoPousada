# apps/quarto/tests/test_forms.py
import pytest
from apps.core.forms import QuartoForm
from apps.core.models.quarto import Quarto

@pytest.mark.django_db
def test_quarto_form_valid_data():
    """Testa se o QuartoForm é válido com dados corretos"""
    data = {
        'numero': '101',
        'status': True,
        'descricao': 'Quarto confortável com vista para o mar',
        'preco': 250.00
    }
    form = QuartoForm(data=data)
    assert form.is_valid(), form.errors  # Deve ser válido
    quarto = form.save(commit=False)
    assert quarto.numero == '101'
    assert quarto.status is True
    assert quarto.descricao == 'Quarto confortável com vista para o mar'
    assert quarto.preco == 250.00

@pytest.mark.django_db
def test_quarto_form_invalid_data():
    """Testa se o QuartoForm detecta dados inválidos"""
    data = {
        'numero': '',  # Campo obrigatório vazio
        'status': 'notabool',  # Valor inválido para BooleanField
        'descricao': '',  # Campo obrigatório vazio
        'preco': -50  # Valor negativo, se tiver validação
    }
    form = QuartoForm(data=data)
    assert not form.is_valid()  # Deve ser inválido
    # Verifica se os erros existem
    assert 'numero' in form.errors
    assert 'descricao' in form.errors
    assert 'preco' in form.errors or 'status' in form.errors
