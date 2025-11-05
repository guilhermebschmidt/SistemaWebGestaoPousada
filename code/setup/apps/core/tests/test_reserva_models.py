import pytest
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from apps.core.models import Hospede, Reserva
from apps.financeiro.models import Titulo


def test_reserva_str(reserva):
    assert str(reserva).startswith(f"Reserva #{reserva.id}")

def test_reserva_save_calcula_valores(reserva, quarto):
    """Testa se o .save() calcula dias e valor total corretamente."""
    assert reserva.quantidade_dias == 3
    assert reserva.valor == 600.00 # 3 dias * R$ 200.00 (do quarto)

@pytest.mark.django_db
def test_reserva_save_cria_titulos_financeiros(reserva, hospede, quarto):
    """
    TESTE DE INTEGRAÇÃO CRÍTICO:
    Verifica se salvar uma *nova* reserva cria os 2 títulos financeiros.
    """
    # A fixture 'reserva' já chamou o .save()
    assert Titulo.objects.filter(reserva=reserva).count() == 2

    sinal = Titulo.objects.get(reserva=reserva, descricao__startswith='Sinal')
    restante = Titulo.objects.get(reserva=reserva, descricao__startswith='Pagamento Restante')

    # Testa o Título 1 (Sinal de 50%)
    assert sinal.valor == 300.00 # 50% de 600
    assert sinal.data_pagamento is not None # Sinal é "pago" na hora

    # Testa o Título 2 (Restante)
    assert restante.valor == 300.00 # 50% de 600
    assert restante.data_pagamento is None # Restante fica em aberto
    assert restante.data_vencimento == reserva.data_reserva_inicio

@pytest.mark.django_db
def test_reserva_save_atualiza_titulos_financeiros(reserva, quarto):
    """
    TESTE DE INTEGRAÇÃO CRITICO:
    Verifica se atualizar uma reserva (datas ou quarto) atualiza os tttulos.
    """
    # Cenario: A reserva ja existe e o sinal (R$ 300) NÃO foi pago
    sinal = Titulo.objects.get(reserva=reserva, descricao__startswith='Sinal')
    restante = Titulo.objects.get(reserva=reserva, descricao__startswith='Pagamento Restante')
    
    # Simula que o sinal ainda não foi pago (para permitir alteração)
    sinal.data_pagamento = None
    sinal.save()

    # Ação: Mudar a reserva de 3 para 5 dias
    reserva.data_reserva_fim = reserva.data_reserva_fim + timedelta(days=2)
    reserva.save() # Deve recalcular (R$ 1000) e atualizar os títulos
    
    sinal.refresh_from_db()
    restante.refresh_from_db()

    # Verificação:
    assert reserva.valor == 1000.00 # 5 dias * R$ 200.00
    assert sinal.valor == 500.00 # 50% de 1000
    assert restante.valor == 500.00 # 50% de 1000