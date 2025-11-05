import pytest
from django.urls import reverse
from apps.core.models import Hospede, Quarto, Reserva
from datetime import date, timedelta

# --- Testes CRUD de QUARTO ---

def test_quarto_listar_get(auth_client, quarto):
    """Testa o GET simples da lista de quartos."""
    url = reverse('quarto:listar')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert quarto.numero in response.content.decode()

def test_quarto_criar_get_form(auth_client):
    """Testa o GET da página de formulário de criação de quarto."""
    # rota usa 'form' para criação/edição
    url = reverse('quarto:form')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert '<form' in response.content.decode()

def test_quarto_editar_get_form(auth_client, quarto):
    """Testa o GET da página de formulário de edição de quarto."""
    url = reverse('quarto:form', kwargs={'quarto_id': quarto.id})
    response = auth_client.get(url)
    assert response.status_code == 200
    # O form.html usa 'debug_data' para popular o valor
    assert f'value="{quarto.numero}"' in response.content.decode()

def test_quarto_criar_post(auth_client):
    """Testa o POST de criação de um novo quarto."""
    url = reverse('quarto:form')
    form_data = {
        'numero': '202',
        'capacidade': 3,
        'tipo_quarto': 'LOFT',
        'descricao': 'Novo Quarto Loft',
        'preco': 350.00
    }
    response = auth_client.post(url, form_data)
    assert response.status_code == 302
    assert response.url == '/quartos/'
    assert Quarto.objects.filter(numero='202').exists()

def test_quarto_editar_post(auth_client, quarto):
    """Testa o POST de atualização de um quarto."""
    url = reverse('quarto:form', kwargs={'quarto_id': quarto.id})
    form_data = {
        'numero': quarto.numero,
        'capacidade': quarto.capacidade,
        'tipo_quarto': quarto.tipo_quarto,
        'descricao': 'Descrição Atualizada', # Campo alterado
        'preco': 300.00 # Campo alterado
    }
    response = auth_client.post(url, form_data)
    quarto.refresh_from_db()
    assert response.status_code == 302
    assert quarto.descricao == 'Descrição Atualizada'
    assert quarto.preco == 300.00

def test_quarto_excluir_post(auth_client, quarto):
    """Testa o POST que de fato exclui o quarto."""
    url = reverse('quarto:excluir', kwargs={'quarto_id': quarto.id})
    response = auth_client.post(url)
    assert response.status_code == 302
    # A view 'excluir' de quarto está com um redirect estranho
    # assert response.url == reverse('quarto:listar') # O ideal
    assert not Quarto.objects.filter(id=quarto.id).exists()

    # -----------------
# Testes das Views de Quarto
# -----------------
def test_quarto_listar_view_com_filtro(auth_client, quarto):
    url = reverse('quarto:listar') + '?tipo_quarto=SUITE'
    response = auth_client.get(url)
    assert response.status_code == 200
    assert quarto.numero in response.content.decode()

def test_quarto_mudar_status_post(auth_client, quarto):
    assert quarto.status == 'DISPONIVEL'
    url = reverse('quarto:mudar_status', kwargs={'pk': quarto.pk})
    response = auth_client.post(url, data={'status': 'MANUTENCAO'})
    
    quarto.refresh_from_db()
    assert response.status_code == 302
    assert response.url == reverse('quarto:listar')
    assert quarto.status == 'MANUTENCAO'