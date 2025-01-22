from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from urllib.parse import urljoin
from contact.models import Chamado, DetalheTarefaPreenchido, Imagem
from weasyprint import HTML

def gerar_pdf_documentacao(chamado, base_url, logo_url, detalhes_preenchidos, template_path, attachment_name):
    for detalhe in detalhes_preenchidos:
        if not detalhe.observacao:
            detalhe.observacao = 'N/A'
        if detalhe.concluido is True:
            detalhe.concluido = 'OK'
        elif detalhe.concluido is False:
            detalhe.concluido = 'N/A'
            
        detalhe.fotos_clientes_url = [
            urljoin(base_url, img.imagem.url)
            for img in Imagem.objects.filter(detalhe_tarefa=detalhe, tipo_imagem='cliente')
        ]
        detalhe.fotos_ajustes_url = [
            urljoin(base_url, img.imagem.url)
            for img in Imagem.objects.filter(detalhe_tarefa=detalhe, tipo_imagem='ajuste')
        ]

    context = {
        'chamado': chamado,
        'detalhes_preenchidos': detalhes_preenchidos,
        'base_url': base_url,
        'logo_url': logo_url,
    }

    html_string = render_to_string(template_path, context)
    html = HTML(string=html_string)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{attachment_name}"'
    html.write_pdf(response)

    return response

@login_required
def download_documentacao_chamado_pdf(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    detalhes_preenchidos = DetalheTarefaPreenchido.objects.filter(chamado=chamado)
    base_url = request.build_absolute_uri('/')
    logo_url = urljoin(base_url, 'static/images/logo_docs.png')

    attachment_name = f"documentacao_chamado_{chamado.id}.pdf"

    template_path = 'contact/documentacao_chamado_pdf.html'

    return gerar_pdf_documentacao(chamado, base_url, logo_url, detalhes_preenchidos, template_path, attachment_name)

@login_required
def documentacao_sem_fotos(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    detalhes_preenchidos = DetalheTarefaPreenchido.objects.filter(chamado=chamado)
    base_url = request.build_absolute_uri('/')
    logo_url = urljoin(base_url, 'static/images/logo_docs.png')

    for detalhe in detalhes_preenchidos:
        if not detalhe.observacao:
            detalhe.observacao = 'N/A'
        if detalhe.concluido is True:
            detalhe.concluido = 'OK'
        elif detalhe.concluido is False:
            detalhe.concluido = 'N/A'

    context = {
        'chamado': chamado,
        'detalhes_preenchidos': detalhes_preenchidos,
        'base_url': base_url, 
        'logo_url': logo_url,
    }

    html_string = render_to_string('contact/doc_chamado_sem_foto.html', context)
    html = HTML(string=html_string)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="documentacao_chamado_{chamado_id}_sem_fotos.pdf"'
    html.write_pdf(response)

    return response
