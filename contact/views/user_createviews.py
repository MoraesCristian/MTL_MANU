from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from contact.forms.create_user import UsuarioCreationForm

@login_required
def create_user_view(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return redirect('profile')  
    else:
        form = UsuarioCreationForm(request=request)
    return render(request, 'contact/create_user.html', {'form': form})
