from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    usuario = request.user  # Obtém o objeto Usuario associado ao User
    return render(request, 'contact/profile.html', {'usuario': usuario})