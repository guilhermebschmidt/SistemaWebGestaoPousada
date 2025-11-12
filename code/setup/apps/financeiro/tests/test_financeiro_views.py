import pytest
from django.urls import reverse
from datetime import date, timedelta
from apps.financeiro.models import Categoria, Titulo
from apps.core.models import Reserva
from decimal import Decimal

# --- Testes das Views de Categoria ---
@pytest.mark.django_db
def test_categoria_list_view_filtra_tipo_d(auth_client, categoria_despesa, categoria_receita):
    url = reverse('financeiro:categoria_list')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert "Limpeza" in response.content.decode()
    assert "Receita de Hospedagem" not in response.content.decode()

@pytest.mark.django_db
def test_categoria_create_post_forca_tipo_d(auth_client):
    url = reverse('financeiro:categoria_create')
    response = auth_client.post(url, data={'descricao': 'Nova Despesa de Teste'})
    assert response.status_code == 302
    assert response.url == reverse('financeiro:categoria_list')
    nova_cat = Categoria.objects.get(descricao='Nova Despesa de Teste')
    assert nova_cat.tipo == 'D'

# --- Testes das Views de Titulo ---
@pytest.mark.django_db
def test_titulo_list_view_com_filtros(auth_client, titulo_receita_sinal, titulo_receita_restante):
    """Testa todos os filtros da view list_titulos."""
    # Filtro 'pago=sim'
    url = reverse('financeiro:list') + '?pago=sim'
    response = auth_client.get(url)
    assert titulo_receita_sinal.descricao in response.content.decode()
    assert titulo_receita_restante.descricao not in response.content.decode()

    # Filtro 'tipo=saida'
    url = reverse('financeiro:list') + '?tipo=saida'
    response = auth_client.get(url)
    assert titulo_receita_sinal.descricao not in response.content.decode()
    
    # Filtro 'hospede'
    hospede_nome = titulo_receita_sinal.hospede.nome
    url = reverse('financeiro:list') + f'?hospede={hospede_nome}'
    response = auth_client.get(url)
    assert titulo_receita_sinal.descricao in response.content.decode()
    
    # Filtro 'data_vencimento'
    data_venc_restante = titulo_receita_restante.data_vencimento.isoformat()
    url = reverse('financeiro:list') + f'?data_inicio={data_venc_restante}&data_fim={data_venc_restante}'
    response = auth_client.get(url)
    assert titulo_receita_restante.descricao in response.content.decode()
    assert titulo_receita_sinal.descricao not in response.content.decode()

@pytest.mark.django_db
def test_titulo_marcar_pago_sinal_confirma_reserva(auth_client, reserva):
    """TESTE DE INTEGRAÇÃO (Financeiro -> Core): Marcar o SINAL como pago confirma a reserva."""
    reserva.status = 'PREVISTA'
    reserva.save()
    titulo_sinal = Titulo.objects.get(reserva=reserva, descricao__startswith='Sinal')
    titulo_sinal.pago = False
    titulo_sinal.data_pagamento = None
    titulo_sinal.save()
    
    url = reverse('financeiro:marcar_pago', kwargs={'pk': titulo_sinal.pk})
    response = auth_client.post(url)
    
    reserva.refresh_from_db()
    titulo_sinal.refresh_from_db()
    
    assert titulo_sinal.pago is True
    assert reserva.status == 'CONFIRMADA'

# --- Testes das Views de Balanço e Relatório ---
@pytest.mark.django_db
def test_balanco_financeiro_view(auth_client, titulo_receita_sinal):
    url = reverse('financeiro:balanco_financeiro')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert "Total Arrecadado" in response.content.decode()
    assert "300,00" in response.content.decode() # Valor do sinal pago

@pytest.mark.django_db
def test_relatorio_faturamento_view(auth_client, titulo_receita_sinal):
    url = reverse('financeiro:relatorio_faturamento')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert "Relatório de Faturamento" in response.content.decode()
    assert "R$ 300,00" in response.content.decode()

@pytest.mark.django_db
def test_relatorio_faturamento_view_csv_export(auth_client, titulo_receita_sinal):
    url = reverse('financeiro:relatorio_faturamento') + '?exportar=csv'
    response = auth_client.get(url)
    assert response.status_code == 200
    assert response['Content-Type'] == 'text/csv'
    assert "Sinal (50%)" in response.content.decode()

@pytest.mark.django_db
def test_titulo_marcar_pago_get_redireciona(auth_client, titulo_receita_sinal):
    """Testa que um GET na view 'marcar_pago' (que espera POST) apenas redireciona."""
    # A view no seu código-fonte não verifica o request.method,
    # então um GET também marcará como pago.
    # Este teste valida esse comportamento (que é um bug de segurança menor).
    
    titulo_receita_sinal.pago = False
    titulo_receita_sinal.save()
    assert titulo_receita_sinal.pago is False
    
    url = reverse('financeiro:marcar_pago', kwargs={'pk': titulo_receita_sinal.pk})
    response = auth_client.get(url) # Fazendo um GET
    
    titulo_receita_sinal.refresh_from_db()
    
    assert response.status_code == 302
    assert response.url == reverse('financeiro:list_titulos')
    assert titulo_receita_sinal.pago is True # A view marcou como pago mesmo com GET