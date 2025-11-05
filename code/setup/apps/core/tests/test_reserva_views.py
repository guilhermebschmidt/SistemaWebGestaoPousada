import pytest
from django.urls import reverse
from apps.core.models import Hospede, Quarto, Reserva
from datetime import date, timedelta

# --- Testes CRUD de RESERVA ---

def test_reserva_listar_get(auth_client, reserva):
    """Testa o GET simples da lista de reservas."""
    url = reverse('reserva:list')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert str(reserva.id_hospede.nome) in response.content.decode()

def test_reserva_criar_get_form(auth_client):
    """Testa o GET da página de formulário de criação de reserva."""
    url = reverse('reserva:criar')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert 'data_reserva_inicio' in response.content.decode()

def test_reserva_editar_get_form(auth_client, reserva):
    """Testa o GET da página de formulário de edição de reserva."""
    url = reverse('reserva:editar', kwargs={'pk': reserva.id})
    response = auth_client.get(url)
    assert response.status_code == 200
    assert reserva.id_hospede.nome in response.content.decode()

def test_reserva_list_checkin_get(auth_client):
    url = reverse('reserva:list_checkin')
    response = auth_client.get(url)
    assert response.status_code == 200

def test_reserva_list_checkout_get(auth_client):
    url = reverse('reserva:list_checkout')
    response = auth_client.get(url)
    assert response.status_code == 200

# -----------------
# Testes das Views de Reserva
# -----------------
def test_reserva_form_post_com_conflito(auth_client, reserva, hospede, quarto):
    """Testa se a view de reserva bloqueia datas conflitantes."""
    url = reverse('reserva:criar')
    
    # Datas conflitantes com a 'reserva' da fixture
    data_inicio = reserva.data_reserva_inicio + timedelta(days=1)
    data_fim = reserva.data_reserva_fim - timedelta(days=1)
    
    form_data = {
        "hospede_nome": hospede.nome,
        "id_hospede": hospede.id,
        "id_quarto": quarto.id,
        "data_reserva_inicio": data_inicio.isoformat(),
        "data_reserva_fim": data_fim.isoformat()
    }
    
    response = auth_client.post(url, form_data)
    assert response.status_code == 200 # Re-renderiza o form
    assert "ERRO: O quarto selecionado já está reservado" in response.content.decode()

def test_reserva_marcar_checkin_post(auth_client, reserva):
    """Testa se a view de check-in atualiza a reserva E o quarto."""
    assert reserva.status == 'PREVISTA'
    assert reserva.id_quarto.status == 'DISPONIVEL'
    
    url = reverse('reserva:checkin', kwargs={'pk': reserva.pk})
    response = auth_client.post(url) # POST é o comportamento correto
    
    reserva.refresh_from_db()
    reserva.id_quarto.refresh_from_db()
    
    assert response.status_code == 302
    assert reserva.status == 'ATIVA'
    assert reserva.data_check_in is not None
    assert reserva.id_quarto.status == 'OCUPADO'

def test_reserva_cancelar_post(auth_client, reserva):
    url = reverse('reserva:cancelar', kwargs={'pk': reserva.pk})
    response = auth_client.post(url, data={'motivo_cancelamento': 'Teste'})
    
    reserva.refresh_from_db()
    assert response.status_code == 302
    assert reserva.status == 'CANCELADA'
    assert reserva.motivo_cancelamento == 'Teste'

def test_reserva_buscar_hospedes_json(auth_client, hospede):
    url = reverse('reserva:buscar_hospedes') + f'?term={hospede.nome}'
    response = auth_client.get(url)
    json_response = response.json()
    
    assert response.status_code == 200
    assert len(json_response) == 1
    assert json_response[0]['id'] == hospede.id
    assert json_response[0]['label'] == hospede.nome