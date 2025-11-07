import pytest
from django.urls import reverse
from apps.core.models import Hospede, Reserva
from datetime import date

@pytest.mark.django_db
def test_hospede_listar_get(auth_client, hospede):
    url = reverse('hospede:listar')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert hospede.nome in response.content.decode()

@pytest.mark.django_db
def test_hospede_criar_get_form(auth_client):
    url = reverse('hospede:criar')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert '<form' in response.content.decode()
    assert 'Adicionar Hóspede' in response.content.decode()

@pytest.mark.django_db
def test_hospede_editar_get_form(auth_client, hospede):
    url = reverse('hospede:editar', kwargs={'cpf': hospede.cpf})
    response = auth_client.get(url)
    assert response.status_code == 200
    assert hospede.nome in response.content.decode()
    assert 'Editar Hóspede' in response.content.decode()

@pytest.mark.django_db
def test_hospede_detalhes_get(auth_client, hospede):
    url = reverse('hospede:detalhes', kwargs={'cpf': hospede.cpf})
    response = auth_client.get(url)
    assert response.status_code == 200
    assert hospede.email in response.content.decode()

@pytest.mark.django_db
def test_hospede_historico_get(auth_client, hospede, reserva):
    url = reverse('hospede:historico', kwargs={'cpf': hospede.cpf})
    response = auth_client.get(url)
    assert response.status_code == 200
    assert f"Reserva #{reserva.id}" in response.content.decode()

@pytest.mark.django_db
def test_hospede_excluir_get_confirm(auth_client, hospede):
    url = reverse('hospede:excluir', kwargs={'cpf': hospede.cpf})
    response = auth_client.get(url)
    assert response.status_code == 200
    assert "Tem certeza que deseja excluir" in response.content.decode()

@pytest.mark.django_db
def test_hospede_excluir_post_sucesso(auth_client, hospede):
    url = reverse('hospede:excluir', kwargs={'cpf': hospede.cpf})
    response = auth_client.post(url)
    assert response.status_code == 302
    assert response.url == '/hospedes/'
    assert not Hospede.objects.filter(cpf=hospede.cpf).exists()

@pytest.mark.django_db
def test_hospede_excluir_post_com_reserva_ativa(auth_client, reserva):
    hospede = reserva.id_hospede
    url = reverse('hospede:excluir', kwargs={'cpf': hospede.cpf})
    response = auth_client.post(url)
    
    assert response.status_code == 302 # Redireciona de volta
    assert response.url == '/hospedes/'
    assert "Este hóspede não pode ser excluído" in auth_client.cookies['messages'].value
    assert Hospede.objects.filter(cpf=hospede.cpf).exists()

@pytest.mark.django_db
def test_hospede_buscar_get(auth_client, hospede):
    url = reverse('hospede:buscar') + f'?search={hospede.nome}'
    response = auth_client.get(url)
    assert response.status_code == 200
    assert hospede.nome in response.content.decode()

@pytest.mark.django_db
def test_hospede_form_create_post_sucesso(auth_client):
    """Testa a nova view (hospede_form) que usa form.is_valid()."""
    url = reverse('hospede:criar')
    form_data = {
        "nome": "Novo Hóspede", "cpf": "11122233344", "passaporte": "",
        "data_nascimento": "1985-01-01", "telefone": "11977776666",
        "email": "novo.hospede@email.com", "rua": "Rua Nova", "numero": "1",
        "bairro": "Bairro", "cidade": "Cidade", "cep": "12345"
    }
    response = auth_client.post(url, form_data)
    assert response.status_code == 302
    assert response.url == reverse('hospede:listar')
    assert Hospede.objects.filter(cpf="11122233344").exists()

@pytest.mark.django_db
def test_hospede_form_post_invalido(auth_client):
    """Testa se a view hospede_form trata erros de validação."""
    url = reverse('hospede:criar')
    form_data = {"nome": "Novo Hóspede", "cpf": "", "passaporte": ""} # Sem CPF/Passaporte
    response = auth_client.post(url, form_data)
    assert response.status_code == 200 # Re-renderiza o form
    assert "É obrigatório fornecer um CPF ou um número de Passaporte." in response.content.decode()


@pytest.mark.django_db
def test_hospede_editar_post_sucesso(auth_client, hospede):
    """Testa o POST de edição de um hospede (usando a view hospede_form)."""
    url = reverse('hospede:editar', kwargs={'cpf': hospede.cpf})
    form_data = {
        "nome": "Hóspede Nome Editado", # Campo alterado
        "cpf": hospede.cpf,
        "passaporte": hospede.passaporte,
        "data_nascimento": hospede.data_nascimento.isoformat(),
        "telefone": "11911112222", # Campo alterado
        "email": hospede.email,
        "rua": hospede.rua, "numero": hospede.numero,
        "bairro": hospede.bairro, "cidade": hospede.cidade, "cep": hospede.cep
    }
    
    response = auth_client.post(url, form_data)
    assert response.status_code == 302 # Redireciona
    assert response.url == reverse('hospede:listar')
    
    hospede.refresh_from_db()
    assert hospede.nome == "Hóspede Nome Editado"
    assert hospede.telefone == "11911112222"