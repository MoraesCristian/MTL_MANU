from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from contact.forms.create_user import UsuarioCreationForm
from contact.models import Usuario
from django.shortcuts import render, get_object_or_404

@login_required
def list_users_view(request):
    if not request.user.is_authenticated:
        return render(request, 'contact/unauthorized.html')
    usuarios = Usuario.objects.none()

    if request.user.tipo_usuario == 'admin':
        usuarios = Usuario.objects.all()
    elif request.user.tipo_usuario == 'operador':
        usuarios = Usuario.objects.filter(tipo_usuario__in=['operador', 'manager', 'user'])
    elif request.user.tipo_usuario == 'manager':
        usuarios = Usuario.objects.none()
    elif request.user.tipo_usuario == 'user':
        usuarios = Usuario.objects.none()

    return render(request, 'contact/list_user.html', {'usuarios': usuarios})


@login_required
def create_user_view(request):
    if request.user.tipo_usuario not in ['admin', 'operador']:
        return render(request, 'contact/list_user.html')

    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST, request=request)
        if form.is_valid():
            user = form.save()
            return redirect('contact:user_detail', user_id=user.id)
    else:
        form = UsuarioCreationForm(request=request)
    return render(request, 'contact/create_user.html', {'form': form})


@login_required
def user_detail_view(request, user_id):
    user = get_object_or_404(Usuario, id=user_id)
    return render(request, 'contact/user_detail.html', {'usuario': user})


@login_required
def edit_user_view(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST, instance=usuario, request=request)
        if form.is_valid():
            form.save()
            return render(request, 'contact/user_detail.html', {'usuario': usuario})
    else:
        form = UsuarioCreationForm(instance=usuario, request=request)
    return render(request, 'contact/edit_user.html', {'form': form, 'usuario': usuario})