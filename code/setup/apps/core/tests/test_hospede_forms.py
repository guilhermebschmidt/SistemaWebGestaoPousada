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
    assert form.is_valid()


@pytest.mark.django_db
def test_hospede_form_cpf_invalido():
    form_data = {
        "nome": "João Silva",
        "cpf": "123ABC456",
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
        "telefone": "telefone123",
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
        "email": "joaosilvaemail"
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
        "data_nascimento": future_date,
        "telefone": "11999999999",
        "email": "joao.silva@test.com"
    }
    form = HospedeForm(data=form_data)
    assert not form.is_valid()
    assert "A data de nascimento não pode ser futura." in form.errors["data_nascimento"]


@pytest.mark.django_db
def test_hospede_form_menor_de_idade():
    menor = date.today().replace(year=date.today().year - 17)
    form_data = {
        "nome": "Pedro Menor",
        "cpf": "98765432100",
        "data_nascimento": menor.isoformat(),
        "telefone": "11988887777",
        "email": "pedro@test.com"
    }
    form = HospedeForm(data=form_data)
    assert not form.is_valid()
    assert "O hóspede deve ter 18 anos ou mais." in form.errors["data_nascimento"]


@pytest.mark.django_db
def test_hospede_form_ano_vigente():
    ano_atual = date.today().replace(month=1, day=1)
    form_data = {
        "nome": "Teste Atual",
        "cpf": "99999999999",
        "data_nascimento": ano_atual.isoformat(),
        "telefone": "11911112222",
        "email": "teste@ano.com"
    }
    form = HospedeForm(data=form_data)
    assert not form.is_valid()
    assert "A data de nascimento não pode ser no ano atual" in form.errors["data_nascimento"][0]


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
    for campo in ["nome", "cpf", "data_nascimento", "telefone", "email"]:
        assert "Este campo é obrigatório." in form.errors[campo]
