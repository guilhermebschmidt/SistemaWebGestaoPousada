import pytest
from apps.core.models.quarto import Quarto

@pytest.mark.django_db
def test_create_quarto():
    """Testa a criação de um objeto Quarto"""
    quarto = Quarto.objects.create(
        numero="101",
        status='DISPONIVEL',
        descricao="Quarto com vista para o mar",
        preco=250.75,
        capacidade=2
    )

    saved_quarto = Quarto.objects.get(numero="101")
    assert saved_quarto.status == 'DISPONIVEL'
    assert saved_quarto.descricao == "Quarto com vista para o mar"
    assert saved_quarto.preco == 250.75

@pytest.mark.django_db
def test_quarto_str_method():
    """Testa o método __str__ do model Quarto"""
    quarto = Quarto.objects.create(
        numero="102",
        status='OCUPADO',
        descricao="Quarto padrão",
        preco=150.00,
        capacidade=2
    )
    assert str(quarto) == "Quarto 102"

@pytest.mark.django_db
def test_quarto_fields_properties():
    """Verifica propriedades dos campos do model"""
    field_numero = Quarto._meta.get_field('numero')
    field_descricao = Quarto._meta.get_field('descricao')
    field_preco = Quarto._meta.get_field('preco')

    assert field_numero.max_length == 100
    assert field_descricao.max_length == 100
    assert field_preco.max_digits == 10
    assert field_preco.decimal_places == 2
    assert field_preco.default == 0.00

@pytest.mark.django_db
def test_quarto_db_table():
    """Verifica se o db_table está correto"""
    # migrations set the table name; allow both legacy 'quarto' and current default 'core_quarto'
    assert Quarto._meta.db_table in ("quarto", "core_quarto")
