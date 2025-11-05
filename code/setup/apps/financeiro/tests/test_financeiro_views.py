import pytest
from django.urls import reverse
from datetime import date
from apps.financeiro.models import Categoria, Titulo
from apps.core.models import Reserva

# --- Testes CRUD de CATEGORIA ---

def test_categoria_criar_get_form(auth_client):
    """Testa o GET da página de formulário de criação de Categoria."""
    url = reverse('financeiro:categoria_create')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert 'Nova Categoria de Despesa' in response.content.decode()

# --- Testes CRUD de TITULO ---

def test_titulo_listar_get(auth_client, titulo_receita):
    """Testa o GET simples da lista de títulos."""
    url = reverse('financeiro:list')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert titulo_receita.descricao in response.content.decode()

def test_titulo_criar_get_form(auth_client):
    """Testa o GET da página de formulário de criação de Título."""
    url = reverse('financeiro:form')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert 'Novo Título Financeiro' in response.content.decode()

def test_titulo_editar_get_form(auth_client, titulo_receita):
    """Testa o GET da página de formulário de edição de Título."""
    url = reverse('financeiro:update', kwargs={'pk': titulo_receita.id})
    response = auth_client.get(url)
    assert response.status_code == 200
    assert titulo_receita.descricao in response.content.decode()

def test_titulo_criar_post_despesa(auth_client, categoria_despesa):
    """Testa o POST de criação de um Título de despesa avulso."""
    url = reverse('financeiro:form')
    form_data = {
        'descricao': "Despesa Avulsa",
        'valor': 50.00,
        'tipo_documento': 'dinheiro',
        'conta_corrente': 'Caixa',
        'data': date.today().isoformat(),
        'data_vencimento': date.today().isoformat(),
        'categoria': categoria_despesa.id,
        'tipo': False, # Saída
        'cancelado': False,
        'pago': True,
        'data_pagamento': date.today().isoformat(),
    }
    response = auth_client.post(url, form_data)
    assert response.status_code == 302
    assert response.url == reverse('financeiro:list')
    assert Titulo.objects.filter(descricao="Despesa Avulsa").exists()

def test_titulo_editar_post(auth_client, titulo_receita):
    """Testa o POST de atualização de um Título."""
    url = reverse('financeiro:update', kwargs={'pk': titulo_receita.id})
    form_data = {
        'descricao': "Sinal Atualizado", # Campo alterado
        'valor': titulo_receita.valor,
        'tipo_documento': titulo_receita.tipo_documento,
        'conta_corrente': titulo_receita.conta_corrente,
        'data': titulo_receita.data.isoformat(),
        'data_vencimento': titulo_receita.data_vencimento.isoformat(),
        'reserva': titulo_receita.reserva.id,
        'tipo': titulo_receita.tipo,
        'cancelado': False,
        'pago': False,
    }
    response = auth_client.post(url, form_data)
    titulo_receita.refresh_from_db()
    assert response.status_code == 302
    assert titulo_receita.descricao == "Sinal Atualizado"

# -----------------
# Testes das Views de Categoria (CBV)
# -----------------
def test_categoria_list_view(auth_client, categoria_despesa, categoria_receita):
    """Testa se a lista de categorias mostra APENAS despesas."""
    url = reverse('financeiro:categoria_list')
    response = auth_client.get(url)
    
    assert response.status_code == 200
    assert "Limpeza" in response.content.decode() # Despesa
    assert "Receita de Hospedagem" not in response.content.decode() # Receita

def test_categoria_create_post(auth_client):
    """Testa se a view de criação força o tipo 'D' (Despesa)."""
    url = reverse('financeiro:categoria_create')
    response = auth_client.post(url, data={'descricao': 'Nova Despesa'})
    
    assert response.status_code == 302 # Redireciona
    nova_cat = Categoria.objects.get(descricao='Nova Despesa')
    assert nova_cat.tipo == 'D'

# -----------------
# Testes das Views de Titulo (FBV)
# -----------------
def test_titulo_list_view_filtros(auth_client, titulo_receita, reserva):
    """Testa se os filtros da lista de títulos funcionam."""
    # Filtro de Tipo (Entrada)
    url = reverse('financeiro:list') + '?tipo=entrada'
    response = auth_client.get(url)
    assert response.status_code == 200
    assert titulo_receita.descricao in response.content.decode()

    # Filtro de Hóspede
    url = reverse('financeiro:list') + f'?hospede={reserva.id_hospede.nome}'
    response = auth_client.get(url)
    assert response.status_code == 200
    assert titulo_receita.descricao in response.content.decode()
    
    # Filtro de Hóspede Inexistente
    url = reverse('financeiro:list') + '?hospede=Inexistente'
    response = auth_client.get(url)
    assert response.status_code == 200
    assert titulo_receita.descricao not in response.content.decode()

@pytest.mark.django_db
def test_titulo_marcar_pago_confirma_reserva(auth_client, reserva):
    """
    TESTE DE INTEGRAÇÃO CRÍTICO:
    Verifica se marcar um título como pago também confirma a reserva.
    """
    # A reserva começa como 'PREVISTA'
    assert reserva.status == 'PREVISTA'
    
    # Pegamos o título de sinal da reserva, que está em aberto
    titulo_sinal = Titulo.objects.get(reserva=reserva, descricao__startswith='Sinal')
    titulo_sinal.pago = False
    titulo_sinal.data_pagamento = None
    titulo_sinal.save()
    
    # Ação: Chamamos a view para marcar o título como pago
    url = reverse('financeiro:marcar_pago', kwargs={'pk': titulo_sinal.pk})
    response = auth_client.post(url) # A view usa POST
    
    # Verificação:
    assert response.status_code == 302
    
    # Recarrega os objetos do banco
    reserva.refresh_from_db()
    titulo_sinal.refresh_from_db()
    
    assert titulo_sinal.pago is True
    assert titulo_sinal.data_pagamento is not None
    assert reserva.status == 'CONFIRMADA'