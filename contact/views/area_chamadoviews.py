import base64
from contact.models import Chamado, Chat, MensagemChat, Tarefa,DetalheTarefa, DetalheTarefaPreenchido,Imagem,ImagemChamado
from contact.forms.chamado_forms import MensagemChatForm
from contact.forms.tarefa_forms import DetalheTarefaPreenchidoForm
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils import timezone
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from PIL import Image
import io



@login_required
def visualizar_chamado(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    chat, created = Chat.objects.get_or_create(chamado=chamado)
    mensagens = chat.mensagens.all()

    if request.method == 'POST':
        form = MensagemChatForm(request.POST)
        if form.is_valid():
            mensagem = form.save(commit=False)
            mensagem.chat = chat
            mensagem.usuario = request.user
            mensagem.save()
            return redirect('contact:visualizar_chamado', chamado_id=chamado.id)
    else:
        form = MensagemChatForm()
        
    context = {
        'chamado': chamado,
        'chat': chat,
        'mensagens': mensagens,
        'form': form
    }
    return render(request, 'contact/visualizar_chamado.html', context)


@login_required
def load_chat(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    chat, created = Chat.objects.get_or_create(chamado=chamado)
    
    if request.method == 'POST':
        mensagem_texto = request.POST.get('mensagem')
        imagem = request.FILES.get('imagem')
        
        if mensagem_texto or imagem:
            mensagem = MensagemChat.objects.create(
                chat=chat, 
                usuario=request.user, 
                conteudo=mensagem_texto, 
                imagem=imagem,
                empresa=request.user.empresa  # supondo que o usuário tem um campo de empresa
            )
            return redirect('contact:load_chat', chamado_id=chamado.id)
        else:
            error = "Mensagem vazia."
    else:
        error = None

    mensagens = chat.mensagens.all()
    context = {
        'mensagens': mensagens,
        'chamado': chamado,
        'error': error
    }
    return render(request, 'contact/chat.html', context)


@login_required
def load_informacao_chamado(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    imagens = ImagemChamado.objects.filter(chamado=chamado)
    user_tipo = request.user.tipo_usuario 
    
    context = {
        'chamado': chamado,
        'empresa': chamado.empresa,
        'prestadora_servico': chamado.prestadora_servico,
        'tecnico_responsavel': chamado.tecnico_responsavel,
        'imagens': imagens,
        'user_tipo': user_tipo,  
    }
    return render(request, 'contact/informacao_chamado.html', context)

@login_required
def load_tarefas_a_realizar(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    tarefas = Tarefa.objects.filter(id=chamado.tarefa.id)
    detalhes_tarefas = DetalheTarefa.objects.filter(tarefa=chamado.tarefa)

    context = {
        'chamado': chamado,
        'tarefas': tarefas,
        'detalhes_tarefas': detalhes_tarefas
    }

    return render(request, 'contact/tarefas_a_realizar.html', context)
    
    
@login_required
def detalhe_tarefa_view(request, chamado_id, tarefa_id, detalhe_tarefa_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    detalhe_tarefa = get_object_or_404(DetalheTarefa, id=detalhe_tarefa_id, tarefa=tarefa)

    detalhe_preenchido = DetalheTarefaPreenchido.objects.filter(
        detalhe_tarefa=detalhe_tarefa, chamado=chamado
    ).first()

    imagens_clientes = Imagem.objects.filter(
        detalhe_tarefa=detalhe_preenchido, tipo_imagem='cliente'
    ) 
    imagens_ajustes = Imagem.objects.filter(
        detalhe_tarefa=detalhe_preenchido, tipo_imagem='ajuste'
    )

    context = {
        'chamado': chamado,
        'tarefa': tarefa,
        'detalhe_tarefa': detalhe_tarefa,
        'detalhe_preenchido': detalhe_preenchido,
        'imagens_clientes': imagens_clientes,
        'imagens_ajustes': imagens_ajustes,
    }
    return render(request, 'contact/detalhe_tarefa.html', context)


def processar_imagens(request, detalhe_preenchido, chamado, tarefa, tipo_imagem, imagens_existentes, prefixo_nome):
    contador = imagens_existentes.count() + 1
    for imagem in request.FILES.getlist(prefixo_nome):
        if contador > 4:
            break
        try:
            novo_nome_imagem = f"{chamado.numero_ordem}_detalhe_{tarefa.id}_{tipo_imagem}_{contador}.jpg"
            img = Image.open(imagem)
            img.verify()  # Verifica se é uma imagem válida
            img = Image.open(imagem)  # Reabrir para manipulação
            img_io = io.BytesIO()
            img.save(img_io, format=img.format or 'JPEG')
            img_io.seek(0)
            imagem_final = ContentFile(img_io.read(), name=novo_nome_imagem)
            file_path = default_storage.save(f"imagens/{novo_nome_imagem}", imagem_final)
            Imagem.objects.create(
                detalhe_tarefa=detalhe_preenchido,
                numero_ordem=chamado,
                tarefa=tarefa,
                tipo_imagem=tipo_imagem,
                imagem=file_path
            )
            contador += 1
        except UnidentifiedImageError:
            print(f"Arquivo inválido: {imagem.name}")
        except Exception as e:
            print(f"Erro ao salvar {novo_nome_imagem}: {e}")


@login_required
def detalhe_tarefa_edit_view(request, chamado_id, tarefa_id, detalhe_tarefa_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    detalhe_tarefa = get_object_or_404(DetalheTarefa, id=detalhe_tarefa_id, tarefa=tarefa)
    detalhe_preenchido = DetalheTarefaPreenchido.objects.filter(detalhe_tarefa=detalhe_tarefa, chamado=chamado).first()
    imagens_clientes = Imagem.objects.filter(detalhe_tarefa=detalhe_preenchido, tipo_imagem='cliente')
    imagens_ajustes = Imagem.objects.filter(detalhe_tarefa=detalhe_preenchido, tipo_imagem='ajuste')

    if request.method == 'POST':
        form = DetalheTarefaPreenchidoForm(request.POST, request.FILES, instance=detalhe_preenchido)
        if form.is_valid():
            detalhe_preenchido = form.save(commit=False)
            detalhe_preenchido.detalhe_tarefa = detalhe_tarefa
            detalhe_preenchido.chamado = chamado
            detalhe_preenchido.usuario = request.user
            detalhe_preenchido.save()

            processar_imagens(request, detalhe_preenchido, chamado, tarefa, 'cliente', imagens_clientes, 'fotos_clientes')
            processar_imagens(request, detalhe_preenchido, chamado, tarefa, 'ajuste', imagens_ajustes, 'fotos_ajustes')
            
        return redirect('contact:detalhe_tarefa', chamado.id, tarefa.id, detalhe_tarefa.id)
    
    else:
        form = DetalheTarefaPreenchidoForm(instance=detalhe_preenchido)

    context = {
        'chamado': chamado,
        'tarefa': tarefa,
        'detalhe_tarefa': detalhe_tarefa,
        'detalhe_preenchido': detalhe_preenchido,
        'imagens_clientes': imagens_clientes,
        'imagens_ajustes': imagens_ajustes,
        'form': form,
        'can_delete_images': request.user.tipo_usuario in ['admin', 'operador'],
    }

    return render(request, 'contact/detalhe_tarefa_form.html', context)



@csrf_exempt
def delete_image(request):
    if request.method == 'POST':
        image_id = request.GET.get('image_id')
        if image_id:
            try:
                imagem = Imagem.objects.get(id=image_id)
                imagem.delete()
                return JsonResponse({'status': 'success'})
            except Imagem.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Imagem não encontrada'})
        else:
            return JsonResponse({'status': 'error', 'message': 'ID da imagem não fornecido'})
    return JsonResponse({'status': 'error', 'message': 'Requisição inválida'})

@login_required
def atualizar_status_chamado_view(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)

    if request.method == 'POST':
        novo_status = request.POST.get('status_chamado')

        if novo_status not in ['aberto', 'executando', 'concluido', 'rejeitado', 'assinatura']:
            return redirect('contact:listar_chamados')
        
        redirection_url = 'contact:listar_chamados'
        redirection_args = {}

        if request.user.is_staff or request.user.tipo_usuario == 'operador':
            chamado.status_chamado = novo_status

            if novo_status == 'aberto':
                redirection_url = 'contact:visualizar_chamado'
                redirection_args = {'chamado_id': chamado.id}

            elif novo_status == 'executando':
                chamado.data_inicio_atv = timezone.now()
                redirection_url = 'contact:load_tarefas_a_realizar'
                redirection_args = {'chamado_id': chamado.id}
                
            elif novo_status == 'concluido':
                chamado.data_fim_atv = timezone.now()
                redirection_url = 'contact:view_signature'
                redirection_args = {'chamado_id': chamado.id}

            elif novo_status == 'assinatura':
                chamado.data_fim_chamado = timezone.now()
                redirection_url = 'contact:view_signature'
                redirection_args = {'chamado_id': chamado.id}

            elif novo_status == 'rejeitado':
                redirection_url = 'contact:listar_chamados'

            chamado.save()
            return redirect(redirection_url, **redirection_args)

        elif request.user.is_authenticated:
            if chamado.prestadora_servico == request.user.empresa:
                if novo_status in ['executando', 'concluido', 'assinatura']:
                    chamado.status_chamado = novo_status

                    if novo_status == 'executando':
                        chamado.data_inicio_atv = timezone.now()
                        redirection_url = 'contact:load_tarefas_a_realizar'
                        redirection_args = {'chamado_id': chamado.id}
                    elif novo_status == 'concluido':
                        chamado.data_fim_atv = timezone.now()
                        redirection_url = 'contact:view_signature'
                        redirection_args = {'chamado_id': chamado.id}
                    elif novo_status == 'assinatura':
                        chamado.data_fim_chamado = timezone.now()
                        redirection_url = 'contact:view_signature'
                        redirection_args = {'chamado_id': chamado.id}

                    chamado.save()
                    return redirect(redirection_url, **redirection_args)

        return redirect('contact:listar_chamados')

@csrf_exempt
def save_signature(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)

    if request.method == 'POST':
        assinatura = request.POST.get('assinatura')
        nome_assinante = request.POST.get('nome_assinante')
        email_assinante = request.POST.get('email_assinante')
        cargo_assinante = request.POST.get('cargo_assinante')

        if not assinatura or not nome_assinante or not email_assinante:
            return HttpResponseBadRequest("Todos os campos são obrigatórios.")

        try:
            formato, imgstr = assinatura.split(';base64,')
            img_data = base64.b64decode(imgstr)
            chamado.assinatura.save(f'chamado_{chamado_id}_assinatura.png', ContentFile(img_data), save=True)
            chamado.nome_assinante = nome_assinante
            chamado.email_assinante = email_assinante
            chamado.cargo_assinante = cargo_assinante
            chamado.save()
        except Exception as e:
            return HttpResponseBadRequest(f"Erro ao salvar a assinatura: {str(e)}")

        return HttpResponseRedirect(reverse('contact:view_signature_tecnico', args=[chamado.id]))

    elif request.method == 'GET':
        context = {
            'chamado': chamado,
            'assinatura_existente': chamado.assinatura.url if chamado.assinatura else None,
            'nome_assinante': chamado.nome_assinante,
            'email_assinante': chamado.email_assinante,
            'cargo_assinante': chamado.cargo_assinante,
        }
        return render(request, 'contact/assinature.html', context)

    return HttpResponseBadRequest("Método não permitido.")

@csrf_exempt
def save_signature_tecnico(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)

    if request.method == 'POST':
        assinatura_tecnico = request.POST.get('assinatura_tecnico')
        nome_tecnico = request.POST.get('nome_tecnico')

        if not assinatura_tecnico or not nome_tecnico:
            return HttpResponseBadRequest("Todos os campos são obrigatórios.")

        try:
            formato, imgstr = assinatura_tecnico.split(';base64,')
            img_data = base64.b64decode(imgstr)
            chamado.assinatura_tecnico.save(f'chamado_{chamado_id}_ass_tecnico.png', ContentFile(img_data), save=True)
            chamado.nome_tecnico = nome_tecnico
            chamado.data_fim_chamado = timezone.now() 
            chamado.status_chamado = 'concluido'
            chamado.save()
        except Exception as e:
            return HttpResponseBadRequest(f"Erro ao salvar a assinatura: {str(e)}")

        return HttpResponseRedirect(reverse('contact:documentacao_chamado', args=[chamado.id]))

    elif request.method == 'GET':
        context = {
            'chamado': chamado,
            'assinatura_existente': chamado.assinatura_tecnico.url if chamado.assinatura_tecnico else None,
            'nome_tecnico': chamado.nome_tecnico,
        }
        return render(request, 'contact/assinature_tecnico.html', context)

    return HttpResponseBadRequest("Método não permitido.")


def view_signature(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    context = {
        'chamado': chamado,
        'assinatura_existente': chamado.assinatura.url if chamado.assinatura else None,
        'nome_assinante': chamado.nome_assinante,
        'email_assinante': chamado.email_assinante,
        'cargo_assinante': chamado.cargo_assinante,        
    }
    return render(request, 'contact/assinature_view.html', context)

def view_signature_tecnico(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    context = {
        'chamado': chamado,
        'assinatura_existente': chamado.assinatura_tecnico.url if chamado.assinatura_tecnico else None,
        'nome_tecnico': chamado.nome_tecnico
    }
    return render(request, 'contact/assinature_view_tecnico.html', context)

@login_required
def documentacao_chamado_view(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    detalhes_preenchidos = DetalheTarefaPreenchido.objects.filter(chamado=chamado)

    for detalhe in detalhes_preenchidos:
        detalhe.fotos_clientes = Imagem.objects.filter(tipo_imagem='cliente', detalhe_tarefa=detalhe)
        detalhe.fotos_ajustes = Imagem.objects.filter(tipo_imagem='ajuste', detalhe_tarefa=detalhe)
    
    context = {
        'chamado': chamado,
        'detalhes_preenchidos': detalhes_preenchidos,
    }
    return render(request, 'contact/documentacao_chamado.html', context)
