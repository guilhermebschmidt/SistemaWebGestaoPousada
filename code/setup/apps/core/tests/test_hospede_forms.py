import pytest
from datetime import date, timedelta
from apps.core.forms import HospedeForm
from apps.core.models import Hospede # Para teste de duplicidade

@pytest.mark.django_db
def test_hospede_form_cpf_invalido_letras():
    form_data = {"cpf": "123ABC456"}
    form = HospedeForm(data=form_data)
    assert not form.is_valid()
    assert "O CPF deve conter apenas números." in form.errors["cpf"]

@pytest.mark.django_db
def test_hospede_form_cpf_invalido_tamanho():
    form_data = {"cpf": "123456"}
    form = HospedeForm(data=form_data)
    assert not form.is_valid()
    assert "O CPF deve conter exatamente 11 dígitos." in form.errors["cpf"]

@pytest.mark.django_db
def test_hospede_form_telefone_invalido():
    form_data = {"telefone": "telefone123"}
    form = HospedeForm(data=form_data)
    assert not form.is_valid()
    assert "O telefone deve conter apenas números." in form.errors["telefone"]

@pytest.mark.django_db
def test_hospede_form_email_invalido():
    form_data = {"email": "joaosilvaemail"}
    form = HospedeForm(data=form_data)
    assert not form.is_valid()
    assert "Insira um email válido." in form.errors["email"]

@pytest.mark.django_db
def test_hospede_form_data_nascimento_futura():
    future_date = (date.today() + timedelta(days=5)).isoformat()
    form = HospedeForm(data={"data_nascimento": future_date})
    assert not form.is_valid()
    assert "A data de nascimento não pode ser futura." in form.errors["data_nascimento"]

@pytest.mark.django_db
def test_hospede_form_menor_de_idade():
    menor = date.today().replace(year=date.today().year - 17)
    form = HospedeForm(data={"data_nascimento": menor.isoformat()})
    assert not form.is_valid()
    assert "O hóspede deve ter 18 anos ou mais." in form.errors["data_nascimento"]

@pytest.mark.django_db
def test_hospede_form_ano_vigente():
    ano_atual = date.today().replace(month=1, day=1)
    form = HospedeForm(data={"data_nascimento": ano_atual.isoformat()})
    assert not form.is_valid()
    assert "A data de nascimento não pode ser no ano atual" in form.errors["data_nascimento"][0]


@pytest.mark.django_db
def test_hospede_form_valid_cpf(db):
    """Testa um hospede válido com CPF."""
    form_data = {
        "nome": "João Silva", "cpf": "123.456.789-00", "passaporte": "",
        "data_nascimento": "1990-05-20", "telefone": "(11) 99999-9999",
        "email": "joao.silva@test.com", "rua": "Rua", "numero": "1",
        "bairro": "Bairro", "cidade": "Cidade", "cep": "12345-678"
    }
    form = HospedeForm(data=form_data)
    assert form.is_valid(), form.errors
    assert form.cleaned_data['cpf'] == '12345678900'
    assert form.cleaned_data['telefone'] == '11999999999'

@pytest.mark.django_db
def test_hospede_form_valid_passaporte(db):
    """Testa um hospede válido com Passaporte."""
    form_data = {
        "nome": "John Smith", "cpf": "", "passaporte": " ABC123456 ",
        "data_nascimento": "1990-05-20", "telefone": "11999999999",
        "email": "john.smith@test.com", "rua": "Rua", "numero": "1",
        "bairro": "Bairro", "cidade": "Cidade", "cep": "12345-678"
    }
    form = HospedeForm(data=form_data)
    assert form.is_valid(), form.errors
    assert form.cleaned_data['passaporte'] == 'ABC123456'

@pytest.mark.django_db
def test_hospede_form_erro_cpf_e_passaporte_juntos(db):
    form_data = {"cpf": "12345678900", "passaporte": "ABC123456"}
    form = HospedeForm(data=form_data)
    assert not form.is_valid()
    assert "Forneça apenas o CPF ou o Passaporte, não ambos." in form.non_field_errors()

@pytest.mark.django_db
def test_hospede_form_erro_sem_cpf_ou_passaporte(db):
    form_data = {"cpf": "", "passaporte": ""}
    form = HospedeForm(data=form_data)
    assert not form.is_valid()
    assert "É obrigatório fornecer um CPF ou um número de Passaporte." in form.non_field_errors()

@pytest.mark.django_db
def test_hospede_form_erro_cpf_duplicado(hospede):
    """Testa a checagem de CPF duplicado (hospede da fixture já existe)."""
    form_data = {"cpf": hospede.cpf, "passaporte": ""} # CPF já existe
    form = HospedeForm(data=form_data)
    assert not form.is_valid()
    assert "Este CPF já está cadastrado para outro hóspede." in form.non_field_errors()

@pytest.mark.django_db
def test_hospede_form_editar_sem_erro_duplicidade(hospede):
    """Testa se, ao editar, o form não acusa o CPF do próprio hóspede como duplicado."""
    form_data = {"cpf": hospede.cpf, "passaporte": "", "nome": "Nome Novo"}
    # Passamos 'instance=hospede' para simular uma edição
    form = HospedeForm(data=form_data, instance=hospede)
    # O form deve ser válido (assumindo que os outros campos obrigatórios estão ok)
    # Aqui, testamos apenas se o erro de duplicidade NÃO é levantado
    assert "Este CPF já está cadastrado" not in str(form.errors)