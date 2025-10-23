import csv
from django.http import HttpResponse

"""
Arquivo com as funções reutilizáveis de exportação CSV e PDF
"""

def exportar_relatorio_csv (nome_arquivo_base, cabecalhos, dados_linhas, request=None):

    data_inicio_str = request.GET.get('data_inicio', '') if request else ''
    data_fim_str = request.GET.get('data_fim', '') if request else ''
    filename_parts = [nome_arquivo_base]

    if data_inicio_str:
        filename_parts.append(f"de_{data_inicio_str}")

    if data_fim_str:
        filename_parts.append(f"ate_{data_fim_str}")

    filename = "_".join(filename_parts) + ".csv"

    response = HttpResponse(
        content_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )

    writer = csv.writer(response)

    if cabecalhos:
        writer.writerow(cabecalhos)
    
    if dados_linhas:
        for linha in dados_linhas:
            writer.writerow(linha)

    return response