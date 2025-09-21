import pytest
from django.urls import reverse
from apps.core.models.quarto import Quarto

@pytest.mark.django_db
class TestQuartoViews:

    @pytest.fixture
    def quarto(self):
        return Quarto.objects.create(
            numero="101",
            status=True,
            descricao="Quarto de teste",
            preco=150.50
        )

    def test_index_view(self, client):
        url = reverse('quarto_index')  # ajuste o nome correto na urls.py
        response = client.get(url)
        assert response.status_code == 200

    def test_quartos_view(self, client, quarto):
        url = reverse('quartos_list')  # ajuste o nome correto na urls.py
        response = client.get(url)
        assert response.status_code == 200
        assert "101" in response.content.decode()

    def test_form_view_get_create(self, client):
        url = reverse('quarto_form_create')  # URL para criar quarto
        response = client.get(url)
        assert response.status_code == 200

    def test_form_view_get_update(self, client, quarto):
        url = reverse('quarto_form_update', args=[quarto.id])  # URL para editar quarto
        response = client.get(url)
        assert response.status_code == 200
        assert "101" in response.content.decode()

    def test_form_view_post_create(self, client):
        url = reverse('quarto_form_create')
        data = {
            'numero': '102',
            'status': True,
            'descricao': 'Quarto novo',
            'preco': 200.00
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert Quarto.objects.filter(numero='102').exists()

    def test_form_view_post_update(self, client, quarto):
        url = reverse('quarto_form_update', args=[quarto.id])
        data = {
            'numero': '101A',
            'status': False,
            'descricao': 'Quarto atualizado',
            'preco': 180.00
        }
        response = client.post(url, data)
        assert response.status_code == 302
        quarto.refresh_from_db()
        assert quarto.numero == '101A'
        assert quarto.status is False
        assert quarto.preco == 180.00

    def test_tipos_quarto_view(self, client):
        url = reverse('quarto_tipos')  # URL para a página de tipos de quarto
        response = client.get(url)
        assert response.status_code == 200

    def test_excluir_quarto_get(self, client, quarto):
        url = reverse('quarto_excluir', args=[quarto.id])
        response = client.get(url)
        assert response.status_code == 200
        assert "101" in response.content.decode()

    def test_excluir_quarto_post(self, client, quarto):
        url = reverse('quarto_excluir', args=[quarto.id])
        response = client.post(url)
        assert response.status_code == 302
        assert not Quarto.objects.filter(id=quarto.id).exists()
