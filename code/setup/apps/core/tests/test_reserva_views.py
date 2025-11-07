import pytest
from django.urls import reverse
from apps.core.models import Reserva, Hospede
from datetime import date, timedelta

@pytest.mark.django_db
def test_reserva_listar_get_com_filtros(auth_client, reserva):
    url = reverse('reserva:list') + f'?status=PREVISTA&hospede={reserva.id_hospede.nome}&quarto={reserva.id_quarto.id}'
    response = auth_client.get(url)
    assert response.status_code == 200
    assert str(reserva.id_hospede.nome) in response.content.decode()

@pytest.mark.django_db
def test_reserva_criar_get_form(auth_client):
    url = reverse('reserva:criar')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert 'data_reserva_inicio' in response.content.decode()

@pytest.mark.django_db
def test_reserva_form_post_com_conflito(auth_client, reserva, hospede, quarto):
    url = reverse('reserva:criar')
    data_inicio = reserva.data_reserva_inicio + timedelta(days=1)
    data_fim = reserva.data_reserva_fim - timedelta(days=1)
    form_data = {
        "hospede_nome": hospede.nome, "id_hospede": hospede.id,
        "id_quarto": quarto.id, "data_reserva_inicio": data_inicio.isoformat(),
        "data_reserva_fim": data_fim.isoformat(),
        "quantidade_adultos": 1, "quantidade_criancas": 0
    }
    response = auth_client.post(url, form_data)
    assert response.status_code == 200 # Re-renderiza o form
    assert "ERRO DE CONFLITO" in auth_client.cookies['messages'].value

@pytest.mark.django_db
def test_reserva_form_post_excesso_capacidade(auth_client, hospede, quarto):
    url = reverse('reserva:criar')
    data_inicio = date.today() + timedelta(days=3)
    data_fim = data_inicio + timedelta(days=2)
    form_data = {
        "hospede_nome": hospede.nome, "id_hospede": hospede.id,
        "id_quarto": quarto.id, # quarto da fixture tem capacidade 2
        "data_reserva_inicio": data_inicio.isoformat(),
        "data_reserva_fim": data_fim.isoformat(),
        "quantidade_adultos": 2, "quantidade_criancas": 1 # Total 3 pessoas
    }
    response = auth_client.post(url, form_data)
    assert response.status_code == 200 # Re-renderiza o form
    assert "excede a capacidade do quarto (2)" in auth_client.cookies['messages'].value

@pytest.mark.django_db
def test_reserva_marcar_checkin_post(auth_client, reserva):
    assert reserva.status == 'PREVISTA'
    assert reserva.id_quarto.status == 'DISPONIVEL'
    
    url = reverse('reserva:checkin', kwargs={'pk': reserva.pk})
    response = auth_client.post(url)
    
    reserva.refresh_from_db()
    reserva.id_quarto.refresh_from_db()
    
    assert response.status_code == 302
    assert reserva.status == 'ATIVA'
    assert reserva.data_check_in is not None
    assert reserva.id_quarto.status == 'OCUPADO'

@pytest.mark.django_db
def test_reserva_marcar_checkout_post(auth_client, reserva):
    reserva.status = 'ATIVA'
    reserva.id_quarto.status = 'OCUPADO'
    reserva.save()
    
    url = reverse('reserva:checkout', kwargs={'pk': reserva.pk})
    response = auth_client.post(url)
    
    reserva.refresh_from_db()
    reserva.id_quarto.refresh_from_db()
    
    assert response.status_code == 302
    assert reserva.status == 'CONCLUIDA'
    assert reserva.data_check_out is not None
    assert reserva.id_quarto.status == 'DISPONIVEL'

@pytest.mark.django_db
def test_reserva_cancelar_post_sucesso(auth_client, reserva):
    url = reverse('reserva:cancelar', kwargs={'pk': reserva.pk})
    response = auth_client.post(url, data={'motivo_cancelamento': 'Teste'})
    
    reserva.refresh_from_db()
    assert response.status_code == 302
    assert reserva.status == 'CANCELADA'
    assert reserva.motivo_cancelamento == 'Teste'

@pytest.mark.django_db
def test_reserva_cancelar_post_falha_ativa(auth_client, reserva):
    """Testa se não pode cancelar reserva com check-in feito."""
    reserva.status = 'ATIVA'
    reserva.data_check_in = date.today()
    reserva.save()
    
    url = reverse('reserva:cancelar', kwargs={'pk': reserva.pk})
    response = auth_client.post(url, data={'motivo_cancelamento': 'Teste'})
    
    assert response.status_code == 302
    assert "já possui registro de Check-in" in auth_client.cookies['messages'].value
    reserva.refresh_from_db()
    assert reserva.status == 'ATIVA' # Não deve mudar

@pytest.mark.django_db
def test_reserva_enviar_email_post(auth_client, reserva):
    url = reverse('reserva:enviar_confirmacao_email', kwargs={'reserva_id': reserva.id})
    response = auth_client.post(url)
    reserva.refresh_from_db()
    
    assert response.status_code == 302
    assert reserva.email_confirmacao_enviado is True
    assert "E-mail de confirmação enviado" in auth_client.cookies['messages'].value

@pytest.mark.django_db
def test_reserva_editar_post_sucesso(auth_client, reserva, hospede, quarto_grande):
    """Testa o POST de edição de uma reserva."""
    url = reverse('reserva:editar', kwargs={'pk': reserva.id})
    
    # Novas datas e novo quarto (quarto_grande)
    data_inicio = date.today() + timedelta(days=5)
    data_fim = data_inicio + timedelta(days=4)
    
    form_data = {
        "hospede_nome": hospede.nome,
        "id_hospede": hospede.id,
        "id_quarto": quarto_grande.id, # Trocando para o quarto grande
        "data_reserva_inicio": data_inicio.isoformat(),
        "data_reserva_fim": data_fim.isoformat(),
        "quantidade_adultos": 2, 
        "quantidade_criancas": 2 # 4 pessoas
    }
    
    response = auth_client.post(url, form_data)
    assert response.status_code == 302 # Redireciona
    assert response.url == reverse('reserva:list')
    
    reserva.refresh_from_db()
    assert reserva.id_quarto == quarto_grande
    assert reserva.quantidade_dias == 4
    assert reserva.valor == 1200.00 # 4 dias * R$ 300.00 (do quarto_grande)

@pytest.mark.django_db
def test_reserva_cancelar_get_confirm_page(auth_client, reserva):
    """Testa o GET da página de confirmação de cancelamento."""
    url = reverse('reserva:cancelar', kwargs={'pk': reserva.pk})
    response = auth_client.get(url)
    assert response.status_code == 200
    assert "Confirmar Cancelamento da Reserva" in response.content.decode() # (Assumindo título no template)

@pytest.mark.django_db
def test_reserva_search_get(auth_client, reserva):
    """Testa a view de busca de reserva (que parece estar obsoleta, mas testamos)."""
    url = reverse('reserva:search') + f'?q={reserva.id_hospede.nome}'
    response = auth_client.get(url)
    assert response.status_code == 200
    assert str(reserva.id_hospede.nome) in response.content.decode()

@pytest.mark.django_db
def test_reserva_list_checkin_checkout_com_reservas_corretas(auth_client, hospede, quarto):
    """Testa se as listas de check-in/out mostram as reservas corretas."""
    # Reserva para check-in hoje
    reserva_checkin = Reserva(
        id_hospede=hospede, id_quarto=quarto,
        data_reserva_inicio=date.today(),
        data_reserva_fim=date.today() + timedelta(days=2),
        quantidade_adultos=1
    )
    reserva_checkin.save()

    # Reserva para check-out hoje (usa um hóspede diferente para tornar a
    # intenção do teste inequívoca)
    hospede_checkout = Hospede.objects.create(
        passaporte="CHK98765",
        nome="Hóspede Checkout",
        telefone="11988887777",
        email="checkout.teste@email.com",
        data_nascimento=date(1990, 1, 1),
        rua="Rua Teste", numero="45", bairro="Bairro Teste",
        cidade="Cidade Teste", cep="87654321"
    )

    reserva_checkout = Reserva(
        id_hospede=hospede_checkout, id_quarto=quarto,
        data_reserva_inicio=date.today() - timedelta(days=2),
        data_reserva_fim=date.today(),
        quantidade_adultos=1
    )
    reserva_checkout.save()

    # Testa view de check-in
    url_checkin = reverse('reserva:list_checkin')
    response_checkin = auth_client.get(url_checkin)
    assert response_checkin.status_code == 200
    assert str(reserva_checkin.id_hospede.nome) in response_checkin.content.decode()
    assert str(reserva_checkout.id_hospede.nome) not in response_checkin.content.decode()

    # Testa view de check-out
    url_checkout = reverse('reserva:list_checkout')
    response_checkout = auth_client.get(url_checkout)
    assert response_checkout.status_code == 200
    assert str(reserva_checkin.id_hospede.nome) not in response_checkout.content.decode()
    assert str(reserva_checkout.id_hospede.nome) in response_checkout.content.decode()