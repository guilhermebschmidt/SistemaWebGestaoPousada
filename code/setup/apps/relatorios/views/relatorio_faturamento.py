from django.shortcuts import render
from django.db.models import Sum, Count
from apps.financeiro.models.titulo import Titulo
from datetime import date
from dateutil.relativedelta import relativedelta
from apps.relatorios.utils import exportar_relatorio_csv
from reportlab.platypus import Paragraph, Table, TableStyle, SimpleDocTemplate, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.http import HttpResponse
import io


def relatorio_faturamento(request):
    """
    View que gera o relatório de faturamento com filtros por data e opções de exportação.
    Mantém a estrutura original, mas melhora o layout e alinhamento do PDF exportado.
    """

    today = date.today()
    data_inicio_str = request.GET.get('data_inicio', today.replace(day=1).strftime('%Y-%m-%d'))
    data_fim_str = request.GET.get('data_fim', (
        today.replace(day=1) + relativedelta(months=1, days=-1)).strftime('%Y-%m-%d'))
    exportar = request.GET.get('exportar')

    # --- Validação de datas ---
    try:
        data_inicio = date.fromisoformat(data_inicio_str)
        data_fim = date.fromisoformat(data_fim_str)
        if data_inicio > data_fim:
            raise ValueError("Data de início não pode ser posterior à data de fim.")
    except ValueError:
        data_inicio = today.replace(day=1)
        data_fim = today.replace(day=1) + relativedelta(months=1, days=-1)

    # --- Consulta principal ---
    queryset = (
        Titulo.objects.filter(tipo=True, cancelado=False, pago=True)
        .filter(data_pagamento__range=(data_inicio, data_fim))
    )

    total = queryset.aggregate(total=Sum('valor'))['total'] or 0
    quantidade = queryset.aggregate(qtd=Count('id'))['qtd'] or 0
    media = round(total / quantidade, 2) if quantidade > 0 else 0

    # --- Exportação CSV ---
    if exportar == 'csv' and queryset.exists():
        cabecalhos_csv = ['Descrição', 'Valor (R$)', 'Data Pagamento']
        dados_csv = [
            (t.descricao, f"{t.valor:.2f}", t.data_pagamento.strftime('%d/%m/%Y'))
            for t in queryset
        ]
        dados_csv.append(('TOTAL', f"{total:.2f}", ''))
        return exportar_relatorio_csv(
            nome_arquivo_base='relatorio_faturamento',
            cabecalhos=cabecalhos_csv,
            dados_linhas=dados_csv,
            request=request
        )

    # --- Exportação PDF (melhorada) ---
    elif exportar == 'pdf' and queryset.exists():
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio_faturamento.pdf"'

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=40, rightMargin=40, topMargin=50, bottomMargin=40)
        elements = []

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'TitleCustom',
            parent=styles['Title'],
            fontSize=16,
            leading=20,
            alignment=1,  # Centralizado
            textColor=colors.HexColor('#333333'),
            spaceAfter=6,
        )
        subtitle_style = ParagraphStyle(
            'SubtitleCustom',
            parent=styles['Normal'],
            fontSize=10,
            alignment=1,
            textColor=colors.grey,
            spaceAfter=14,
        )

        titulo_pdf = "Relatório de Faturamento"
        periodo_str = f"Período: {data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}"

        # Cabeçalho
        elements.append(Paragraph(titulo_pdf, title_style))
        elements.append(Paragraph(periodo_str, subtitle_style))
        elements.append(Spacer(1, 10))

        # Tabela de dados
        dados_pdf = [
            [Paragraph('<b>Descrição</b>', styles['Normal']),
             Paragraph('<b>Valor (R$)</b>', styles['Normal']),
             Paragraph('<b>Data Pagamento</b>', styles['Normal'])]
        ]

        for t in queryset:
            dados_pdf.append([
                Paragraph(t.descricao or '-', styles['Normal']),
                f"R$ {t.valor:.2f}",
                t.data_pagamento.strftime('%d/%m/%Y') if t.data_pagamento else '-'
            ])

        # Totais
        dados_pdf.append(['', '', ''])
        dados_pdf.append([
            Paragraph('<b>Total:</b>', styles['Normal']),
            Paragraph(f"R$ {total:.2f}", styles['Normal']),
            ''
        ])
        dados_pdf.append([
            Paragraph('<b>Quantidade:</b>', styles['Normal']),
            Paragraph(str(quantidade), styles['Normal']),
            ''
        ])
        dados_pdf.append([
            Paragraph('<b>Média:</b>', styles['Normal']),
            Paragraph(f"R$ {media:.2f}", styles['Normal']),
            ''
        ])

        # Tabela configurada com larguras e estilo visual
        colWidths = [280, 100, 100]
        tabela = Table(dados_pdf, colWidths=colWidths)
        tabela.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E0E0E0')),  # Cabeçalho
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),  # Coluna de valores à direita
            ('ALIGN', (2, 1), (2, -1), 'CENTER'),  # Datas centralizadas
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.whitesmoke, colors.lightgrey]),  # zebra
        ]))

        elements.append(tabela)
        doc.build(elements)

        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    # --- Contexto padrão (exibição na tela) ---
    context = {
        'titulos': queryset,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'total': total,
        'quantidade': quantidade,
        'media': media,
    }

    # Preparar strings de exibição com formatação brasileira (vírgula decimal)
    for t in queryset:
        try:
            t.valor_display = f"R$ {t.valor:.2f}".replace('.', ',')
        except Exception:
            t.valor_display = f"R$ {t.valor}"

    context['total_display'] = f"R$ {total:.2f}".replace('.', ',')
    context['media_display'] = f"R$ {media:.2f}".replace('.', ',') if isinstance(media, (int, float)) else media

    return render(request, 'relatorios/faturamento.html', context)
