from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.urls import path
from contact.views import login_view, home_view, logout_view
from django.shortcuts import redirect

def root_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('home/', login_required(home_view), name='home'),
    path('', root_view, name='root'),  # Define a rota raiz para redirecionar
    path('logout/', logout_view, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
