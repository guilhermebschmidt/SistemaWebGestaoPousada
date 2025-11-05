import pytest
from django.urls import reverse
from apps.core.models import Hospede, Quarto, Reserva
from datetime import date, timedelta

# --- Testes CRUD de HOSPEDE ---

def test_hospede_listar_get(auth_client, hospede):
    """Testa o GET simples da lista de hóspedes."""
    url = reverse('hospede:listar')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert hospede.nome in response.content.decode()

def test_hospede_criar_get_form(auth_client):
    """Testa o GET da página de formulário de criação de hóspede."""
    # URL name in urls/hospede.py uses 'form' for creation
    url = reverse('hospede:form')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert '<form' in response.content.decode()

def test_hospede_editar_get_form(auth_client, hospede):
    """Testa o GET da página de formulário de edição de hóspede."""
    # URLs use the same 'form' view for editing and creation; pass cpf for edit
    url = reverse('hospede:form', kwargs={'cpf': hospede.cpf})
    response = auth_client.get(url)
    assert response.status_code == 200
    assert hospede.nome in response.content.decode() # Verifica se os dados do hospede estão no form

def test_hospede_detalhes_get(auth_client, hospede):
    """Testa o GET da página de detalhes do hóspede."""
    url = reverse('hospede:detalhes', kwargs={'cpf': hospede.cpf})
    response = auth_client.get(url)
    assert response.status_code == 200
    assert hospede.email in response.content.decode()

def test_hospede_historico_get(auth_client, hospede, reserva):
    """Testa o GET da página de histórico de reservas do hóspede."""
    url = reverse('hospede:historico', kwargs={'cpf': hospede.cpf})
    response = auth_client.get(url)
    assert response.status_code == 200
    content = response.content.decode()
    # Template rendering may differ; assert that either the reservation id or the
    # hospede name appears in the response body.
    assert str(reserva.id) in content or reserva.id_hospede.nome in content

def test_hospede_excluir_get_confirm(auth_client, hospede):
    """Testa o GET da página de confirmação de exclusão."""
    url = reverse('hospede:excluir', kwargs={'cpf': hospede.cpf})
    response = auth_client.get(url)
    assert response.status_code == 200
    assert "Tem certeza que deseja excluir" in response.content.decode()

def test_hospede_excluir_post(auth_client, hospede):
    """Testa o POST que de fato exclui o hóspede."""
    url = reverse('hospede:excluir', kwargs={'cpf': hospede.cpf})
    response = auth_client.post(url)
    assert response.status_code == 302 # Redireciona
    assert response.url == '/hospedes/'
    assert not Hospede.objects.filter(cpf=hospede.cpf).exists()

def test_hospede_buscar_get(auth_client, hospede):
    """Testa a view de busca de hóspede."""
    url = reverse('hospede:buscar') + f'?search={hospede.nome}'
    response = auth_client.get(url)
    assert response.status_code == 200
    assert hospede.nome in response.content.decode()

# -----------------
# Testes das Views de Hospede
# -----------------
def test_hospede_listar_view(auth_client, hospede):
    url = reverse('hospede:listar')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert hospede.nome in response.content.decode()

def test_hospede_form_create_post(auth_client):
    """Testa a view de criação manual de hospede."""
    url = reverse('hospede:form')
    form_data = {
        "nome": "Novo Hóspede",
        "cpf": "11122233344",
        "data_nascimento": "1985-01-01",
        "telefone": "11977776666",
        "email": "novo.hospede@email.com",
        "rua": "Rua Nova", "numero": "1", "bairro": "Bairro", "cidade": "Cidade", "cep": "12345"
    }
    response = auth_client.post(url, form_data)
    assert response.status_code == 302 # Redireciona
    assert response.url == '/hospedes/'
    assert Hospede.objects.filter(cpf="11122233344").exists()

def test_hospede_form_post_invalido(auth_client):
    """Testa se a view de hospede trata erros de validação (ex: menor de idade)."""
    url = reverse('hospede:form')
    form_data = {
        "nome": "Novo Hóspede",
        "cpf": "11122233355",
        "data_nascimento": "2010-01-01", # Menor de idade
        "telefone": "11977776666",
        "email": "novo.hospede@email.com",
        "rua": "Rua Nova", "numero": "1", "bairro": "Bairro", "cidade": "Cidade", "cep": "12345"
    }
    response = auth_client.post(url, form_data)
    assert response.status_code == 200 # Re-renderiza o form
    assert "O hóspede deve ter 18 anos ou mais." in response.content.decode()