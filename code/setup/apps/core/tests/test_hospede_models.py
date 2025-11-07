import pytest
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from apps.core.models import Hospede

@pytest.mark.django_db
def test_create_hospede(db):
    hospede = Hospede.objects.create(
        cpf="12345678901", nome="João Silva", telefone="999999999",
        email="joao@email.com", data_nascimento=date(1990, 1, 1),
        rua="Rua", numero="1", bairro="Bairro", cidade="Cidade", cep="12345"
    )
    saved_hospede = Hospede.objects.get(cpf="12345678901")
    assert saved_hospede.nome == "João Silva"

@pytest.mark.django_db
def test_hospede_str_method(db):
    hospede = Hospede.objects.create(
        cpf="98765432100", nome="Maria Souza", telefone="888888888",
        email="maria@email.com", data_nascimento=date(1992, 5, 15),
        rua="Rua", numero="1", bairro="Bairro", cidade="Cidade", cep="12345"
    )
    assert str(hospede) == "Maria Souza"

@pytest.mark.django_db
def test_hospede_db_table(db):
    assert Hospede._meta.db_table == "hospede"


@pytest.mark.django_db
def test_hospede_save_limpa_cpf_e_passaporte(db):
    """Testa se o .save() limpa e formata CPF e Passaporte."""
    hospede = Hospede.objects.create(
        cpf="123.456.789-00",
        nome="Hóspede Formatado",
        telefone="11999998888", email="hospede.cpf@email.com",
        data_nascimento=date(1990, 1, 1),
        rua="Rua", numero="1", bairro="Bairro", cidade="Cidade", cep="12345"
    )
    hospede.refresh_from_db()
    assert hospede.cpf == "12345678900"
    
    hospede_pass = Hospede.objects.create(
        passaporte=" abc 123 ",
        nome="Hóspede Passaporte",
        telefone="11999998888", email="hospede.pass@email.com",
        data_nascimento=date(1990, 1, 1),
        rua="Rua", numero="1", bairro="Bairro", cidade="Cidade", cep="12345"
    )
    hospede_pass.refresh_from_db()
    assert hospede_pass.passaporte == "ABC 123"

@pytest.mark.django_db
def test_hospede_clean_menor_de_idade(db):
    hospede = Hospede(
        cpf="11122233344", nome="Menor Teste", telefone="111", email="menor@email.com",
        data_nascimento = date.today() - timedelta(days=17 * 365) # 17 anos
    )
    with pytest.raises(ValidationError, match="O hóspede deve ter 18 anos ou mais."):
        hospede.save() # .save() agora chama .full_clean()

@pytest.mark.django_db
def test_hospede_clean_data_futura(db):
    hospede = Hospede(
        cpf="11122233355", nome="Viajante do Tempo", telefone="111", email="futuro@email.com",
        data_nascimento = date.today() + timedelta(days=1)
    )
    with pytest.raises(ValidationError, match="A data de nascimento não pode ser futura."):
        hospede.save()

@pytest.mark.django_db
def test_hospede_clean_cpf_e_passaporte_juntos(db):
    hospede = Hospede(
        cpf="11122233366", passaporte="XYZ789", nome="Duplicado", telefone="111", 
        email="duplicado@email.com", data_nascimento=date(1990, 1, 1)
    )
    with pytest.raises(ValidationError, match="Forneça apenas o CPF ou o Passaporte, não ambos."):
        hospede.save()

@pytest.mark.django_db
def test_hospede_clean_sem_cpf_ou_passaporte(db):
    hospede = Hospede(
        cpf=None, passaporte=None, nome="Sem Documento", telefone="111", 
        email="semdoc@email.com", data_nascimento=date(1990, 1, 1)
    )
    with pytest.raises(ValidationError, match="É obrigatório fornecer um CPF ou um número de Passaporte."):
        hospede.save()