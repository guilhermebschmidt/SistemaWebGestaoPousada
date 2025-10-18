from ..models import Reserva
from ..relatorios import ocupacao

'''
View para funções dos relatórios de ocupação e financeiros.
'''

def relatorio_ocupacao(request):
    

    dados_relatorio = ocupacao.gerar_relatorio_de_ocupacao(data_inicio, data_fim)
    
    context = {
        'dados': dados_relatorio,
        # ...
    }
    return render(request, 'core/relatorios/ocupacao.html', context)