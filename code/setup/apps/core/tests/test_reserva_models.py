import pytest
import datetime
from apps.core.models.hospede import Hospede
from apps.core.models.quarto import Quarto
from apps.core.models.reserva import Reserva

@pytest.mark.django_db
def test_create_reserva():
    """Testa a criação de uma reserva com hospede e quarto"""
    hospede = Hospede.objects.create(
        cpf="12345678900",
        nome="João Silva",
        telefone="11999999999",
        email="joao@example.com",
        data_nascimento=datetime.date(1990, 1, 1)
    )
    quarto = Quarto.objects.create(
        numero="101",
        status=True,
        descricao="Quarto deluxe",
        preco=250.00
    )

    reserva = Reserva.objects.create(
        id_hospede=hospede,
        id_quarto=quarto,
        data_reserva_inicio=datetime.date.today() + datetime.timedelta(days=1),
        data_reserva_fim=datetime.date.today() + datetime.timedelta(days=3),
        quantidade_dias=2,
        valor=500.00
    )

    saved_reserva = Reserva.objects.get(id=reserva.id)
    assert saved_reserva.id_hospede == hospede
    assert saved_reserva.id_quarto == quarto
    assert saved_reserva.quantidade_dias == 2
    assert saved_reserva.valor == 500.00

@pytest.mark.django_db
def test_reserva_str_method():
    """Testa o método __str__ do model Reserva"""
    hospede = Hospede.objects.create(
        cpf="98765432100",
        nome="Maria Souza",
        telefone="11988888888",
        email="maria@example.com",
        data_nascimento=datetime.date(1992, 5, 20)
    )
    quarto = Quarto.objects.create(
        numero="102",
        status=True,
        descricao="Quarto standard",
        preco=150.00
    )
    reserva = Reserva.objects.create(
        id_hospede=hospede,
        id_quarto=quarto
    )
    expected_str = f"Reserva #{reserva.id} - Hóspede {hospede} - Quarto {quarto}"
    assert str(reserva) == expected_str

@pytest.mark.django_db
def test_reserva_fields_properties():
    """Verifica propriedades dos campos do model Reserva"""
    field_quantidade_dias = Reserva._meta.get_field('quantidade_dias')
    field_valor = Reserva._meta.get_field('valor')
    field_data_inicio = Reserva._meta.get_field('data_reserva_inicio')
    field_data_fim = Reserva._meta.get_field('data_reserva_fim')

    assert field_quantidade_dias.default == 0
    assert field_valor.max_digits == 10
    assert field_valor.decimal_places == 2
    assert field_valor.default == 0.00
    assert field_data_inicio.null is True
    assert field_data_fim.null is True

@pytest.mark.django_db
def test_reserva_db_table():
    """Verifica se o db_table está correto"""
    assert Reserva._meta.db_table == "reserva"
