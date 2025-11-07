import pytest
from django.db import IntegrityError
from apps.financeiro.models import Banco, Categoria, Titulo

@pytest.mark.django_db
def test_banco_str(db):
    # Use get_or_create to be robust when migrations/seed already created this banco
    banco, created = Banco.objects.get_or_create(
        codigo="001",
        defaults={"descricao": "Banco do Brasil"}
    )
    # A descrição pode variar (seed usa 'Banco do Brasil S.A.'); validar de forma flexível
    assert banco.codigo == "001"
    assert "Banco do Brasil" in banco.descricao

@pytest.mark.django_db
def test_categoria_str(categoria_despesa, categoria_receita):
    assert str(categoria_despesa) == "Limpeza (Despesa)"
    assert str(categoria_receita) == "Receita de Hospedagem (Receita)"

@pytest.mark.django_db
def test_categoria_unique_together(db):
    """Testa se (tipo, descricao) são únicos."""
    # Garantir estado limpo para este par (tipo, descricao) caso uma seed/migration
    # ou outro fixture já tenha criado a mesma combinação.
    Categoria.objects.filter(tipo='D', descricao='Duplicada').delete()

    Categoria.objects.create(tipo='D', descricao='Duplicada')
    # Garantir que o IntegrityError por duplicação seja isolado sem quebrar a transação
    from django.db import transaction
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            Categoria.objects.create(tipo='D', descricao='Duplicada')

    # Garante que a regra é por tipo
    Categoria.objects.create(tipo='R', descricao='Duplicada') # Isso DEVE funcionar
    # Contagem mínima: assegura que as criadas estão presentes (pode haver outras seeds)
    assert Categoria.objects.filter(descricao='Duplicada').count() >= 2

@pytest.mark.django_db
def test_titulo_str(titulo_receita_sinal):
    assert str(titulo_receita_sinal) == f"{titulo_receita_sinal.descricao} - {titulo_receita_sinal.valor}"

@pytest.mark.django_db
def test_titulo_tipo_display_method(titulo_receita_sinal):
    titulo_receita_sinal.tipo = True # Entrada
    assert titulo_receita_sinal.tipo_display() == "Entrada"
    
    titulo_receita_sinal.tipo = False # Saída
    assert titulo_receita_sinal.tipo_display() == "Saída"