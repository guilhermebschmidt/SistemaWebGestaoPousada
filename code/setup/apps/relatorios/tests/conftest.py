import pytest
from decimal import Decimal
from datetime import date, timedelta
from apps.financeiro.models import Categoria, Titulo

@pytest.fixture
def titulo_receita_sinal(db):
    """
    Cria um Título de receita, pago, no valor de 300,
    que corresponde aos filtros da view 'relatorio_faturamento'.
    """
    
    # 1. Cria uma Categoria (necessária para o Título)
    categoria, _ = Categoria.objects.get_or_create(
        nome="Sinal de Reserva",
        tipo='receita'
    )
    
    # Define uma data de referência para o teste
    hoje = date.today()

    # 2. Cria o Título com TODOS os campos obrigatórios
    titulo = Titulo.objects.create(
        # --- Campos que correspondem ao filtro da VIEW ---
        tipo=True,      
        pago=True,       
        cancelado=False, 
        valor=Decimal('300.00'),
        data_pagamento=hoje,
        
        tipo_documento='pix', 
        descricao="Sinal (50%)",
        conta_corrente="Conta Teste", 
        data=hoje, 
        data_vencimento=hoje + timedelta(days=30), 
        
        id_categoria=categoria, 
    )
    return titulo