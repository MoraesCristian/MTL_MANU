from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from urllib.parse import urljoin
from contact.models import Chamado, DetalheTarefaPreenchido, Imagem,ImagemChamado
from weasyprint import HTML
from datetime import timedelta

def gerar_pdf_documentacao(chamado, base_url, logo_url, detalhes_preenchidos, template_path, attachment_name):
    analista = chamado.analista_resp
    if analista:
        analista_nome = f"{analista.first_name} {analista.last_name}".strip()
        analista_email = analista.email
    else:
        analista_nome = "Nenhum analista definido"
        analista_email = "N/A"
    
    tecnicos = chamado.tecnicos_responsaveis.all()
    
    imagens_urls = [
    urljoin(base_url, imagem.imagem.url)
    for imagem in ImagemChamado.objects.filter(chamado=chamado)
]
    
    if chamado.data_inicio_atv and chamado.data_fim_chamado:
        data_inicio_formatada = chamado.data_inicio_atv.strftime('%d/%m/%Y')
        data_fim_formatada = chamado.data_fim_chamado.strftime('%d/%m/%Y')

        delta = chamado.data_fim_chamado - chamado.data_inicio_atv
        dias = delta.days
        horas = delta.seconds // 3600
        minutos = (delta.seconds % 3600) // 60
        duracao_formatada = f"{dias} dias, {horas} horas e {minutos} minutos"
    else:
        data_inicio_formatada = "N/A"
        data_fim_formatada = "N/A"
        duracao_formatada = "Data de início ou fim não definida"


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
        'analista_nome': analista_nome,
        'analista_email': analista_email,
        'tecnicos': tecnicos,
        'duracao_chamado': duracao_formatada,
        'imagens_urls': imagens_urls,
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

    attachment_name = f"DocPreventiva_{chamado.numero_ordem}.pdf"

    template_path = 'contact/documentacao_chamado_pdf.html'

    return gerar_pdf_documentacao(chamado, base_url, logo_url, detalhes_preenchidos, template_path, attachment_name)


@login_required
def down_doc_fotos_emrg_corre(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    detalhes_preenchidos = DetalheTarefaPreenchido.objects.filter(chamado=chamado)
    base_url = request.build_absolute_uri('/')
    logo_url = urljoin(base_url, 'static/images/logo_docs.png')

    attachment_name = f"Doc_{chamado.numero_ordem}.pdf"

    template_path = 'contact/doc_pdf_corre.html'

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
