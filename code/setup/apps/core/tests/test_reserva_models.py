import pytest
from datetime import date, timedelta
from apps.core.models import Reserva
from apps.financeiro.models import Titulo
from decimal import Decimal

@pytest.mark.django_db
def test_reserva_str(reserva):
    assert str(reserva) == f"Reserva #{reserva.id} - 2 pessoa(s) - Quarto {reserva.id_quarto}"

@pytest.mark.django_db
def test_reserva_save_calcula_valores(reserva, quarto):
    assert reserva.quantidade_dias == 3
    assert reserva.valor == 600.00 # 3 dias * R$ 200.00 (do quarto)
    assert reserva.numero_total_hospedes == 2

@pytest.mark.django_db
def test_reserva_save_cria_titulos_financeiros(reserva, hospede):
    """TESTE DE INTEGRAÇÃO (Reserva -> Financeiro): Verifica a criação automática dos títulos."""
    assert Titulo.objects.filter(reserva=reserva).count() == 2

    sinal = Titulo.objects.get(reserva=reserva, descricao__startswith='Sinal')
    restante = Titulo.objects.get(reserva=reserva, descricao__startswith='Pagamento Restante')

    assert sinal.valor == Decimal("300.00")
    assert sinal.data_pagamento is not None

    assert restante.valor == Decimal("300.00")
    assert restante.data_pagamento is None
    assert restante.data_vencimento == reserva.data_reserva_inicio

@pytest.mark.django_db
def test_reserva_save_atualiza_titulos_financeiros(reserva, quarto_grande):
    """TESTE DE INTEGRAÇÃO (Reserva -> Financeiro): Verifica a atualização dos títulos."""
    sinal = Titulo.objects.get(reserva=reserva, descricao__startswith='Sinal')
    restante = Titulo.objects.get(reserva=reserva, descricao__startswith='Pagamento Restante')
    sinal.data_pagamento = None
    sinal.save()

    reserva.id_quarto = quarto_grande
    reserva.save() 
    
    sinal.refresh_from_db()
    restante.refresh_from_db()

    assert reserva.valor == Decimal("900.00") # 3 dias * R$ 300.00
    assert sinal.valor == Decimal("450.00")
    assert restante.valor == Decimal("450.00")