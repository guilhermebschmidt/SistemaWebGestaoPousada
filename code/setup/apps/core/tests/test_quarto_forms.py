import pytest
from apps.core.forms import QuartoForm, QuartoStatusForm

@pytest.mark.django_db
def test_quarto_form_valid(db):
    form_data = {
        "numero": "102",
        "capacidade": 2,
        "tipo_quarto": "SUITE",
        "descricao": "Teste",
        "preco": 250.00
    }
    form = QuartoForm(data=form_data)
    assert form.is_valid(), form.errors

@pytest.mark.django_db
def test_quarto_form_invalid_data(db):
    """Testa se o QuartoForm detecta dados inválidos (campos obrigatórios)."""
    data = {
        'numero': '', 'capacidade': '', 'tipo_quarto': '',
        'descricao': '', 'preco': ''
    }
    form = QuartoForm(data=data)
    assert not form.is_valid()
    assert 'numero' in form.errors
    assert 'capacidade' in form.errors
    assert 'tipo_quarto' in form.errors
    assert 'preco' in form.errors
    # Descricao é obrigatória no form (init)
    assert 'descricao' in form.errors 

@pytest.mark.django_db
def test_quarto_status_form_valid(quarto):
    form = QuartoStatusForm(data={'status': 'MANUTENCAO'}, instance=quarto)
    assert form.is_valid()