from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.urls import path, include
from contact.views import login_view, home_view, logout_view
from django.shortcuts import redirect
from contact.views import CustomPasswordResetView

def root_view(request):
    if request.user.is_authenticated:
        return redirect('contact:home')
    else:
        return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('home/',home_view, name='home'),
    path('contact/', include('contact.urls', namespace='contact')),
    path('logout/', logout_view, name='logout'),
    path('', root_view, name='root'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
