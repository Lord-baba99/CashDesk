from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . views import *
import cashdeskapp.urls
import bankapp.urls
import accounts.urls
import enterprise.urls
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('shutdown/', shutdown, name='shutdown'),
    path('caisse/', include(login_required(cashdeskapp.urls))),
    path('banque/', include(login_required(bankapp.urls))),
    path('account/', include(login_required(accounts.urls))),
    path('settings/', include(login_required(enterprise.urls))),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
