from django.shortcuts import render
from django.db.models import Sum, Count
from ..models.titulo import Titulo
import datetime
import io
import csv
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


def relatorio_faturamento(request):
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    exportar = request.GET.get('exportar')  # pode ser 'pdf' ou 'csv'

    queryset = Titulo.objects.filter(tipo=True, cancelado=False, pago=True)

    if data_inicio:
        queryset = queryset.filter(data_pagamento__gte=data_inicio)
    if data_fim:
        queryset = queryset.filter(data_pagamento__lte=data_fim)

    total = queryset.aggregate(total=Sum('valor'))['total'] or 0
    quantidade = queryset.aggregate(qtd=Count('id'))['qtd'] or 0
    media = round(total / quantidade, 2) if quantidade > 0 else 0

    # Exportar CSV
    if exportar == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="relatorio_faturamento.csv"'
        writer = csv.writer(response)
        writer.writerow(['Descrição', 'Valor', 'Data Pagamento'])
        for t in queryset:
            writer.writerow([t.descricao, t.valor, t.data_pagamento])
        writer.writerow([])
        writer.writerow(['TOTAL', total])
        return response

    # Exportar PDF
    elif exportar == 'pdf':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio_faturamento.pdf"'

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        y = height - 50

        p.setFont("Helvetica-Bold", 14)
        p.drawString(200, y, "Relatório de Faturamento")
        y -= 40
        p.setFont("Helvetica", 10)
        p.drawString(50, y, f"Período: {data_inicio or 'Início'} até {data_fim or 'Hoje'}")
        y -= 20

        p.setFont("Helvetica-Bold", 10)
        p.drawString(50, y, "Descrição")
        p.drawString(300, y, "Valor (R$)")
        p.drawString(450, y, "Data Pagamento")
        y -= 15
        p.line(50, y, 550, y)
        y -= 10

        p.setFont("Helvetica", 9)
        for t in queryset:
            p.drawString(50, y, t.descricao[:40])
            p.drawString(300, y, f"{t.valor:.2f}")
            p.drawString(450, y, t.data_pagamento.strftime('%d/%m/%Y') if t.data_pagamento else '-')
            y -= 15
            if y < 50:
                p.showPage()
                y = height - 50

        y -= 20
        p.setFont("Helvetica-Bold", 10)
        p.drawString(50, y, f"Total Faturado: R$ {total:.2f}")
        p.drawString(300, y, f"Quantidade: {quantidade}")
        p.drawString(450, y, f"Média: R$ {media:.2f}")

        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    # Exibir no navegador
    context = {
        'titulos': queryset,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'total': total,
        'quantidade': quantidade,
        'media': media,
        'hoje': datetime.date.today(),
    }
    return render(request, 'financeiro/relatorio/faturamento.html', context)
