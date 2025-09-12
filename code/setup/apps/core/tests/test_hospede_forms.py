import pytest
from datetime import date, timedelta
from apps.core.forms import HospedeForm

@pytest.mark.django_db
def test_hospede_form_valido():
    form_data = {
        "nome": "João Silva",
        "cpf": "12345678900",
        "data_nascimento": "1990-05-20",
        "telefone": "11999999999",
        "email": "joao.silva@test.com"
    }
    form = HospedeForm(data=form_data)
    assert form.is_valid()  # deve passar

@pytest.mark.django_db
def test_hospede_form_cpf_invalido():
    form_data = {
        "nome": "João Silva",
        "cpf": "123ABC456",  # inválido
        "data_nascimento": "1990-05-20",
        "telefone": "11999999999",
        "email": "joao.silva@test.com"
    }
    form = HospedeForm(data=form_data)
    assert not form.is_valid()
    assert "O CPF deve conter apenas números." in form.errors["cpf"]

@pytest.mark.django_db
def test_hospede_form_telefone_invalido():
    form_data = {
        "nome": "João Silva",
        "cpf": "12345678900",
        "data_nascimento": "1990-05-20",
        "telefone": "telefone123",  # inválido
        "email": "joao.silva@test.com"
    }
    form = HospedeForm(data=form_data)
    assert not form.is_valid()
    assert "O telefone deve conter apenas números." in form.errors["telefone"]

@pytest.mark.django_db
def test_hospede_form_email_invalido():
    form_data = {
        "nome": "João Silva",
        "cpf": "12345678900",
        "data_nascimento": "1990-05-20",
        "telefone": "11999999999",
        "email": "joaosilvaemail"  # inválido
    }
    form = HospedeForm(data=form_data)
    assert not form.is_valid()
    assert "Insira um email válido." in form.errors["email"]

@pytest.mark.django_db
def test_hospede_form_data_nascimento_futura():
    future_date = (date.today() + timedelta(days=5)).isoformat()
    form_data = {
        "nome": "João Silva",
        "cpf": "12345678900",
        "data_nascimento": future_date,  # futura
        "telefone": "11999999999",
        "email": "joao.silva@test.com"
    }
    form = HospedeForm(data=form_data)
    assert not form.is_valid()
    assert "A data de nascimento não pode ser futura." in form.errors["data_nascimento"]

@pytest.mark.django_db
def test_hospede_form_campos_obrigatorios():
    form_data = {
        "nome": "",
        "cpf": "",
        "data_nascimento": "",
        "telefone": "",
        "email": ""
    }
    form = HospedeForm(data=form_data)
    assert not form.is_valid()
    assert "Este campo é obrigatório." in form.errors["nome"]
    assert "Este campo é obrigatório." in form.errors["cpf"]
    assert "Este campo é obrigatório." in form.errors["data_nascimento"]
    assert "Este campo é obrigatório." in form.errors["telefone"]
    assert "Este campo é obrigatório." in form.errors["email"]
