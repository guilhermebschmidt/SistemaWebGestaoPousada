from django.http import HttpResponse
import csv
import os
from django.conf import settings
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4



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

    # Use 'text/csv' content type (tests expect exact match without charset)
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )

    writer = csv.writer(response)

    if cabecalhos:
        writer.writerow(cabecalhos)
    
    if dados_linhas:
        for linha in dados_linhas:
            writer.writerow(linha)

    return response

def exportar_relatorio_pdf (nome_arquivo_base, titulo_pdf, periodo_str, dados_tabela, request=None):

    data_inicio_str = request.GET.get('data_inicio', '') if request else ''
    data_fim_str = request.GET.get('data_fim', '') if request else ''
    filename_parts = [nome_arquivo_base]

    if data_inicio_str: 
        filename_parts.append(f"de_{data_inicio_str}")
    if data_fim_str:
        filename_parts.append(f"ate_{data_fim_str}")
    filename = "_".join(filename_parts) + ".pdf"
   

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    
    styles = getSampleStyleSheet()
    story = []

    caminho_logo = os.path.join(settings.BASE_DIR, 'static', 'imagens', 'logo_invertido.png')
    print(f"DEBUG: BASE_DIR é: {settings.BASE_DIR}")
    
    try:
        logo = Image(caminho_logo, width=100, height=30) 
        
        tabela_logo = Table([[logo]], colWidths=[doc.width])
        tabela_logo.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'RIGHT'),  
            ('VALIGN', (0,0), (-1,-1), 'TOP')   
        ]))
        story.append(tabela_logo)
        story.append(Spacer(1, 1*cm))
        
    except Exception as e:
        story.append(Paragraph(f"Falha ao carregar imagem: {e}", styles['Normal']))


    titulo = Paragraph(titulo_pdf, styles['h1'])
    story.append(titulo)
    story.append(Spacer(1, 0.2*cm))

    if periodo_str:
        periodo_p = Paragraph(periodo_str, styles['h2'])
        story.append(periodo_p)
        story.append(Spacer(1, 0.5*cm))
    
    if dados_tabela:
        tabela = Table(dados_tabela, colWidths=[11*cm, 6*cm])
    
    tabela_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.gainsboro),  # Cor de fundo do cabeçalho
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),  # Cor do texto do cabeçalho
        ('ALIGN', (0,0), (-1,0), 'CENTER'),               # Alinhamento horizontal do cabeçalho 
        ('FONTNAME', (0,0), (-1,0), 'Helvetica'),         # Fonte do cabeçalho
        ('BOTTOMPADDING', (0,0), (-1,0), 12),             # Espaçamento inferior do cabeçalho

        ('BACKGROUND', (0,1), (-1,-1), colors.white),     # Cor de fundo das linhas de dados
        ('TEXTCOLOR', (0,1), (-1,-1), colors.black),      # Cor do texto das linhas de dados

        ('ALIGN', (0,1), (0,-1), 'LEFT'),                 # Alinha a primeira coluna (Métrica) à esquerda
        ('ALIGN', (1,1), (1,-1), 'LEFT'),                 # Alinha a segunda coluna (Valor) à direita
        ('FONTNAME', (0,1), (0,-1), 'Helvetica'),         # Deixa a primeira coluna em negrito

        ('GRID', (0,0), (-1,-1), 1, colors.black)         # Adiciona bordas (grid) à tabela inteira
    ])
    tabela.setStyle(tabela_style)
    story.append(tabela)

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response