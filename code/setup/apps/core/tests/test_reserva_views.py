import pytest
from django.urls import reverse
from apps.core.models.reserva import Reserva
from apps.core.models.hospede import Hospede
from apps.core.models.quarto import Quarto
import datetime
from django.utils import timezone

@pytest.mark.django_db
class TestReservaViews:

    @pytest.fixture
    def hospede(self):
        return Hospede.objects.create(
            cpf="12345678900",
            nome="Teste Hospede",
            telefone="999999999",
            email="teste@email.com",
            data_nascimento="1990-01-01"
        )

    @pytest.fixture
    def quarto(self):
        return Quarto.objects.create(
            numero="101",
            status=True,
            descricao="Quarto teste",
            preco=150.00
        )

    @pytest.fixture
    def reserva(self, hospede, quarto):
        return Reserva.objects.create(
            id_hospede=hospede,
            id_quarto=quarto,
            data_reserva_inicio=datetime.date.today(),
            data_reserva_fim=datetime.date.today() + datetime.timedelta(days=2),
            quantidade_dias=2,
            valor=300.00
        )

    def test_list_view(self, client, reserva):
        url = reverse('reserva:list')
        response = client.get(url)
        assert response.status_code == 200
        assert str(reserva.id_hospede.nome) in response.content.decode()

    def test_list_checkin_view(self, client, reserva):
        url = reverse('reserva:list_checkin')
        response = client.get(url)
        assert response.status_code == 200
        assert str(reserva.id_hospede.nome) in response.content.decode()

    def test_list_checkout_view(self, client, reserva):
        url = reverse('reserva:list_checkout')
        response = client.get(url)
        assert response.status_code == 200
        assert str(reserva.id_hospede.nome) in response.content.decode()

    def test_add_view_get(self, client):
        url = reverse('reserva:add')
        response = client.get(url)
        assert response.status_code == 200

    def test_add_view_post(self, client, hospede, quarto):
        url = reverse('reserva:add')
        data = {
            'id_hospede': hospede.pk,
            'id_quarto': quarto.pk,
            'data_reserva_inicio': datetime.date.today(),
            'data_reserva_fim': datetime.date.today() + datetime.timedelta(days=3),
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert Reserva.objects.filter(id_hospede=hospede, id_quarto=quarto).exists()

    def test_update_view_get(self, client, reserva):
        url = reverse('reserva:update', args=[reserva.id])
        response = client.get(url)
        assert response.status_code == 200

    def test_update_view_post(self, client, reserva, hospede, quarto):
        url = reverse('reserva:update', args=[reserva.id])
        data = {
            'id_hospede': hospede.pk,
            'id_quarto': quarto.pk,
            'data_reserva_inicio': datetime.date.today(),
            'data_reserva_fim': datetime.date.today() + datetime.timedelta(days=5),
        }
        response = client.post(url, data)
        assert response.status_code == 302
        reserva.refresh_from_db()
        assert reserva.data_reserva_fim == datetime.date.today() + datetime.timedelta(days=5)

    def test_delete_view_get(self, client, reserva):
        url = reverse('reserva:delete', args=[reserva.id])
        response = client.get(url)
        assert response.status_code == 200

    def test_delete_view_post(self, client, reserva):
        url = reverse('reserva:delete', args=[reserva.id])
        response = client.post(url)
        assert response.status_code == 302
        assert not Reserva.objects.filter(id=reserva.id).exists()

    def test_search_view(self, client, reserva):
        url = reverse('reserva:search')
        response = client.get(url, {'q': 'Teste Hospede'})
        assert response.status_code == 200
        assert str(reserva.id_hospede.nome) in response.content.decode()

    def test_marcar_checkin(self, client, reserva):
        url = reverse('reserva:marcar_checkin', args=[reserva.id])
        response = client.post(url)
        reserva.refresh_from_db()
        assert response.status_code == 302
        assert reserva.data_check_in is not None

    def test_marcar_checkout(self, client, reserva):
        url = reverse('reserva:marcar_checkout', args=[reserva.id])
        response = client.post(url)
        reserva.refresh_from_db()
        assert response.status_code == 302
        assert reserva.data_check_out is not None
