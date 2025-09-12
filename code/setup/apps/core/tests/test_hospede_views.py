import pytest
from django.urls import reverse
from apps.core.models.hospede import Hospede

@pytest.mark.django_db
class TestHospedeViews:

    @pytest.fixture
    def hospede(self):
        return Hospede.objects.create(
            cpf="12345678900",
            nome="Teste Hospede",
            telefone="11999999999",
            email="teste@hospede.com",
            data_nascimento="2000-01-01"
        )

    def test_hospede_list_view(self, client, hospede):
        url = reverse('hospede_list')  # /hospede/hospedes/
        response = client.get(url)
        assert response.status_code == 200
        assert hospede.nome in response.content.decode()

    def test_hospede_create_view_get(self, client):
        url = reverse('hospede_create')  # /hospede/hospedes/create/
        response = client.get(url)
        assert response.status_code == 200

    def test_hospede_create_view_post(self, client):
        url = reverse('hospede_create')
        data = {
            'cpf': '11122233344',
            'nome': 'Novo Hospede',
            'telefone': '11988887777',
            'email': 'novo@hospede.com',
            'data_nascimento': '1990-05-05'
        }
        response = client.post(url, data)
        assert response.status_code == 302  # redireciona após criar
        assert Hospede.objects.filter(cpf='11122233344').exists()

    def test_hospede_update_view_get(self, client, hospede):
        url = reverse('hospede_update', args=[hospede.cpf])
        response = client.get(url)
        assert response.status_code == 200

    def test_hospede_update_view_post(self, client, hospede):
        url = reverse('hospede_update', args=[hospede.cpf])
        data = {
            'nome': 'Hospede Atualizado',
            'telefone': hospede.telefone,
            'email': hospede.email,
            'data_nascimento': hospede.data_nascimento
        }
        response = client.post(url, data)
        assert response.status_code == 302
        hospede.refresh_from_db()
        assert hospede.nome == 'Hospede Atualizado'

    def test_hospede_delete_view_get(self, client, hospede):
        url = reverse('hospede_delete', args=[hospede.cpf])
        response = client.get(url)
        assert response.status_code == 200

    def test_hospede_delete_view_post(self, client, hospede):
        url = reverse('hospede_delete', args=[hospede.cpf])
        response = client.post(url)
        assert response.status_code == 302
        assert not Hospede.objects.filter(cpf=hospede.cpf).exists()

    def test_hospede_detail_view(self, client, hospede):
        url = reverse('hospede_detail', args=[hospede.cpf])
        response = client.get(url)
        assert response.status_code == 200
        assert hospede.nome in response.content.decode()

    def test_hospede_search_view_post(self, client, hospede):
        url = reverse('hospede_search')  # /hospede/hospedes/search/
        response = client.post(url, {'search': 'Teste'})
        assert response.status_code == 200
        assert hospede.nome in response.content.decode()
