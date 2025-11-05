import pytest
from django.db import IntegrityError
from apps.financeiro.models import Categoria, Titulo

def test_categoria_str(categoria_despesa, categoria_receita):
    assert str(categoria_despesa) == "Limpeza (Despesa)"
    assert str(categoria_receita) == "Receita de Hospedagem (Receita)"

def test_categoria_unique_together(db):
    """Testa se não é possível criar categorias com mesmo tipo e descrição."""
    Categoria.objects.create(tipo='D', descricao='Duplicada')
    with pytest.raises(IntegrityError):
        Categoria.objects.create(tipo='D', descricao='Duplicada')

def test_titulo_str(titulo_receita):
    assert str(titulo_receita) == f"{titulo_receita.descricao} - {titulo_receita.valor}"

def test_titulo_tipo_display(titulo_receita):
    titulo_receita.tipo = True # Entrada
    assert titulo_receita.tipo_display() == "Entrada"
    
    titulo_receita.tipo = False # Saída
    assert titulo_receita.tipo_display() == "Saída"