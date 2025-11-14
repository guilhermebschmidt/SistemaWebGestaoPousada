import pytest
from django.urls import reverse
from apps.financeiro.models import Categoria, Titulo

@pytest.mark.django_db
def test_relatorio_faturamento_view(auth_client, titulo_receita_sinal):
    data_pagamento = titulo_receita_sinal.data_pagamento
    data_str = data_pagamento.strftime('%Y-%m-%d')
    url = reverse('relatorios:faturamento') + f'?data_inicio={data_str}&data_fim={data_str}'
    response = auth_client.get(url)
    assert response.status_code == 200
    assert "Relatório de Faturamento" in response.content.decode()
    assert "R$ 300,00" in response.content.decode()

@pytest.mark.django_db
def test_relatorio_faturamento_view_csv_export(auth_client, titulo_receita_sinal):
    data_pagamento = titulo_receita_sinal.data_pagamento
    data_str = data_pagamento.strftime('%Y-%m-%d')
    url = reverse('relatorios:faturamento') + f'?data_inicio={data_str}&data_fim={data_str}&exportar=csv'
    response = auth_client.get(url)
    assert response.status_code == 200
    assert response['Content-Type'] == 'text/csv'
    assert "Sinal (50%)" in response.content.decode()
    assert "300.00" in response.content.decode()