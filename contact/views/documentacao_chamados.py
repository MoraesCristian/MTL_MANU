from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa
from urllib.parse import urljoin
from django.conf import settings
from contact.models import Chamado, DetalheTarefaPreenchido

@login_required
def download_documentacao_chamado_pdf(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    detalhes_preenchidos = DetalheTarefaPreenchido.objects.filter(chamado=chamado)
    imagens_clientes = chamado.imagem_set.filter(tipo_imagem='cliente')
    imagens_ajustes = chamado.imagem_set.filter(tipo_imagem='ajuste')

    base_url = request.build_absolute_uri('/')

    for detalhe in detalhes_preenchidos:
        if not detalhe.observacao:
            detalhe.observacao = 'N/A'
        if detalhe.concluido is True:
            detalhe.concluido = 'S'
        elif detalhe.concluido is False:
            detalhe.concluido = 'N/A'
        if detalhe.fotos_clientes:
            detalhe.fotos_clientes_url = urljoin(base_url, detalhe.fotos_clientes.url)
        if detalhe.fotos_ajustes:
            detalhe.fotos_ajustes_url = urljoin(base_url, detalhe.fotos_ajustes.url)

    context = {
        'chamado': chamado,
        'detalhes_preenchidos': detalhes_preenchidos,
        'imagens_clientes': imagens_clientes,
        'imagens_ajustes': imagens_ajustes,
        'base_url': base_url,  # Passa a base URL para o template
    }

    html_string = render_to_string('contact/documentacao_chamado_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="documentacao_chamado_{chamado_id}.pdf"'

    pisa_status = pisa.CreatePDF(html_string, dest=response)

    if pisa_status.err:
        return HttpResponse('Ocorreu um erro ao gerar o PDF', status=500)

    return response

@login_required
def documentacao_sem_fotos(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    detalhes_preenchidos = DetalheTarefaPreenchido.objects.filter(chamado=chamado)

    base_url = request.build_absolute_uri('/')

    for detalhe in detalhes_preenchidos:
        if not detalhe.observacao:
            detalhe.observacao = 'N/A'
        if detalhe.concluido is True:
            detalhe.concluido = 'S'
        elif detalhe.concluido is False:
            detalhe.concluido = 'N/A'

    context = {
        'chamado': chamado,
        'detalhes_preenchidos': detalhes_preenchidos,
        'base_url': base_url,  # Passa a base URL para o template
    }

    html_string = render_to_string('contact/doc_chamado_sem_foto.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="documentacao_chamado_{chamado_id}_sem_fotos.pdf"'

    pisa_status = pisa.CreatePDF(html_string, dest=response)

    if pisa_status.err:
        return HttpResponse('Ocorreu um erro ao gerar o PDF', status=500)

    return response