import pytest
from apps.core.models.hospede import Hospede
import datetime

@pytest.mark.django_db
def test_create_hospede():
    """Testa a criação de um objeto Hospede"""
    hospede = Hospede.objects.create(
        cpf="12345678901",
        nome="João Silva",
        telefone="999999999",
        email="joao@email.com",
        data_nascimento=datetime.date(1990, 1, 1)
    )

    # Verifica se foi salvo no banco
    saved_hospede = Hospede.objects.get(cpf="12345678901")
    assert saved_hospede.nome == "João Silva"
    assert saved_hospede.telefone == "999999999"
    assert saved_hospede.email == "joao@email.com"
    assert saved_hospede.data_nascimento == datetime.date(1990, 1, 1)

@pytest.mark.django_db
def test_hospede_str_method():
    """Testa o método __str__ do model Hospede"""
    hospede = Hospede.objects.create(
        cpf="98765432100",
        nome="Maria Souza",
        telefone="888888888",
        email="maria@email.com",
        data_nascimento=datetime.date(1992, 5, 15)
    )
    assert str(hospede) == "Maria Souza"

@pytest.mark.django_db
def test_hospede_fields_max_length():
    """Testa os max_length dos campos do model"""
    field_nome = Hospede._meta.get_field('nome')
    field_cpf = Hospede._meta.get_field('cpf')
    field_telefone = Hospede._meta.get_field('telefone')
    field_email = Hospede._meta.get_field('email')

    assert field_nome.max_length == 100
    assert field_cpf.max_length == 100
    assert field_telefone.max_length == 100
    assert field_email.max_length == 100

@pytest.mark.django_db
def test_hospede_db_table():
    """Verifica se o db_table está correto"""
    assert Hospede._meta.db_table == "hospede"
