import pytest
from django.urls import reverse
from apps.core.models import Quarto

@pytest.mark.django_db
def test_quarto_listar_get(auth_client, quarto):
    url = reverse('quarto:listar')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert quarto.numero in response.content.decode()

@pytest.mark.django_db
def test_quarto_listar_get_com_filtro(auth_client, quarto, quarto_grande):
    url = reverse('quarto:listar') + '?tipo_quarto=LOFT'
    response = auth_client.get(url)
    assert response.status_code == 200
    assert "Quarto 102" in response.content.decode() # Quarto grande (LOFT)
    assert "Quarto 101" not in response.content.decode() # Quarto (SUITE)

@pytest.mark.django_db
def test_quarto_criar_get_form(auth_client):
    url = reverse('quarto:criar')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert '<form' in response.content.decode()

@pytest.mark.django_db
def test_quarto_editar_get_form(auth_client, quarto):
    url = reverse('quarto:editar', kwargs={'pk': quarto.id})
    response = auth_client.get(url)
    assert response.status_code == 200
    assert f'value="{quarto.numero}"' in response.content.decode()

@pytest.mark.django_db
def test_quarto_criar_post(auth_client):
    url = reverse('quarto:criar')
    form_data = {
        'numero': '202', 'capacidade': 3, 'tipo_quarto': 'LOFT',
        'descricao': 'Novo Quarto Loft', 'preco': 350.00
    }
    response = auth_client.post(url, form_data)
    assert response.status_code == 302
    assert response.url == reverse('quarto:listar')
    assert Quarto.objects.filter(numero='202').exists()

@pytest.mark.django_db
def test_quarto_editar_post(auth_client, quarto):
    url = reverse('quarto:editar', kwargs={'pk': quarto.id})
    form_data = {
        'numero': quarto.numero, 'capacidade': quarto.capacidade,
        'tipo_quarto': quarto.tipo_quarto,
        'descricao': 'Descrição Atualizada', # Campo alterado
        'preco': 300.00 # Campo alterado
    }
    response = auth_client.post(url, form_data)
    quarto.refresh_from_db()
    assert response.status_code == 302
    assert quarto.descricao == 'Descrição Atualizada'
    assert quarto.preco == 300.00

@pytest.mark.django_db
def test_quarto_excluir_post(auth_client, quarto):
    url = reverse('quarto:excluir', kwargs={'pk': quarto.id})
    response = auth_client.post(url)
    assert response.status_code == 302
    assert response.url == reverse('quarto:listar')
    assert not Quarto.objects.filter(id=quarto.id).exists()

@pytest.mark.django_db
def test_quarto_mudar_status_post(auth_client, quarto):
    assert quarto.status == 'DISPONIVEL'
    url = reverse('quarto:mudar_status', kwargs={'pk': quarto.pk})
    response = auth_client.post(url, data={'status': 'MANUTENCAO'})
    
    quarto.refresh_from_db()
    assert response.status_code == 302
    assert response.url == reverse('quarto:listar')
    assert quarto.status == 'MANUTENCAO'


@pytest.mark.django_db
def test_quarto_excluir_get_redireciona(auth_client, quarto):
    """Testa que um GET na view de excluir (que só aceita POST) redireciona."""
    url = reverse('quarto:excluir', kwargs={'pk': quarto.id})
    response = auth_client.get(url)
    
    # A view de excluir do quarto não tem página de confirmação (é um bug de UX)
    # Ela simplesmente redireciona para a lista se não for POST
    assert response.status_code == 302
    assert response.url == reverse('quarto:listar')
    assert Quarto.objects.filter(id=quarto.id).exists() # Garante que não foi excluído

@pytest.mark.django_db
def test_quarto_mudar_status_get_form(auth_client, quarto):
    """Testa o GET da página 'mudar_status'."""
    url = reverse('quarto:mudar_status', kwargs={'pk': quarto.pk})
    response = auth_client.get(url)
    
    assert response.status_code == 200
    assert f"Mudar Status do Quarto {quarto.numero}" in response.content.decode() # (Assumindo que o template tem um título)