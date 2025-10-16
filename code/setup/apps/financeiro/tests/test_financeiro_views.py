import pytest
from django.urls import reverse
from datetime import date
from apps.core.models import Hospede, Quarto, Reserva
from apps.financeiro.models import Categoria, Titulo

@pytest.mark.django_db
class TestFinanceiroViews:

    @pytest.fixture
    def setup_data(self):
        """Fixture completa para criar todos os objetos necessários."""
        hospede = Hospede.objects.create(
            cpf="98765432109", nome="Ana Teste", telefone="11912345678",
            email="ana@teste.com", data_nascimento="1988-08-08"
        )
        quarto = Quarto.objects.create(numero="303", tipo_quarto='FLAT', capacidade=3, preco=300.00)
        reserva = Reserva.objects.create(
            id_hospede=hospede, id_quarto=quarto, status='PREVISTA',
            data_reserva_inicio=date.today(), data_reserva_fim=date.today(), valor=300.00
        )
        categoria = Categoria.objects.create(tipo='R', descricao="Teste de View")
        titulo = Titulo.objects.create(
            descricao="Pagamento Sinal Reserva", valor=150.00, data=date.today(),
            data_vencimento=date.today(), tipo=True, cancelado=False, pago=False,
            reserva=reserva, hospede=hospede, categoria=categoria, tipo_documento='pix',
            conta_corrente='Principal'
        )
        return {'hospede': hospede, 'reserva': reserva, 'categoria': categoria, 'titulo': titulo}

    def test_categoria_list_view(self, authed_client, setup_data):
        """Testa se a página de listagem de categorias carrega."""
        url = reverse('financeiro:categoria_list')
        response = authed_client.get(url)
        assert response.status_code == 200

    def test_titulo_list_view(self, authed_client, setup_data):
        """Testa se a página de listagem de títulos carrega e contém o título."""
        url = reverse('financeiro:list')
        response = authed_client.get(url)
        assert response.status_code == 200
        assert setup_data['titulo'].descricao in response.content.decode()

    def test_titulo_list_view_filter_pago(self, authed_client, setup_data):
        """Testa o filtro 'pago' da listagem de títulos."""
        titulo = setup_data['titulo']
        titulo.pago = True
        titulo.save()

        # Filtra por 'pago=sim'
        url_pago = reverse('financeiro:list') + '?pago=sim'
        response_pago = authed_client.get(url_pago)
        assert titulo.descricao in response_pago.content.decode()

        # Filtra por 'pago=nao'
        url_nao_pago = reverse('financeiro:list') + '?pago=nao'
        response_nao_pago = authed_client.get(url_nao_pago)
        assert titulo.descricao not in response_nao_pago.content.decode()

    def test_titulo_create_view_post(self, authed_client, setup_data):
        """Testa a criação de um novo título via POST."""
        hospede = setup_data['hospede']
        url = reverse('financeiro:form')
        form_data = {
            'descricao': 'Nova Despesa de Teste', 'valor': 75.00, 'tipo_documento': 'dinheiro',
            'conta_corrente': 'Caixa', 'data': date.today().isoformat(),
            'data_vencimento': date.today().isoformat(), 'tipo': 'False',
            'cancelado': 'False', 'pago': 'False', 'hospede': hospede.pk
        }
        response = authed_client.post(url, form_data)
        assert response.status_code == 302  # Redireciona após sucesso
        assert Titulo.objects.filter(descricao='Nova Despesa de Teste').exists()

    def test_titulo_update_view_post(self, authed_client, setup_data):
        """Testa a atualização de um título existente."""
        titulo = setup_data['titulo']
        url = reverse('financeiro:update', args=[titulo.pk])
        form_data = {
            'descricao': 'Descrição Atualizada', 'valor': titulo.valor, 'tipo_documento': titulo.tipo_documento,
            'conta_corrente': titulo.conta_corrente, 'data': titulo.data.isoformat(),
            'data_vencimento': titulo.data_vencimento.isoformat(), 'tipo': 'True',
            'cancelado': 'False', 'pago': 'False', 'reserva': titulo.reserva.pk
        }
        response = authed_client.post(url, form_data)
        assert response.status_code == 302
        titulo.refresh_from_db()
        assert titulo.descricao == 'Descrição Atualizada'

    def test_marcar_pago_view_and_reserva_status_update(self, authed_client, setup_data):
        """
        Testa a view 'marcar_pago' e a interação crítica:
        mudar o status da reserva para 'CONFIRMADA'.
        """
        titulo = setup_data['titulo']
        reserva = setup_data['reserva']
        assert reserva.status == 'PREVISTA'  # Garante o estado inicial

        url = reverse('financeiro:marcar_pago', args=[titulo.pk])
        response = authed_client.get(url)  # Usando GET para a URL da ação

        assert response.status_code == 302  # Deve redirecionar

        # Verifica os efeitos
        titulo.refresh_from_db()
        reserva.refresh_from_db()

        assert titulo.pago is True
        assert titulo.data_pagamento is not None
        assert reserva.status == 'CONFIRMADA'