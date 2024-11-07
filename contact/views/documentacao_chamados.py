from django.http import HttpResponse
from django.template.loader import render_to_string

from contact.models import Chamado, DetalheTarefaPreenchido
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

@login_required
def gerar_pdf_chamado_view(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    detalhes_preenchidos = DetalheTarefaPreenchido.objects.filter(chamado=chamado)

    imagens_clientes = chamado.imagem_set.filter(tipo_imagem='cliente')
    imagens_ajustes = chamado.imagem_set.filter(tipo_imagem='ajuste')

    context = {
        'chamado': chamado,
        'detalhes_preenchidos': detalhes_preenchidos,
        'imagens_clientes': imagens_clientes,
        'imagens_ajustes': imagens_ajustes,
    }

    html_string = render_to_string('contact/documentacao_chamado_pdf.html', context)
    html = HTML(string=html_string)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="documentacao_chamado_{chamado_id}.pdf"'
    html.write_pdf(response)

    return response
