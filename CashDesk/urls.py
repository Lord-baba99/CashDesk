from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . views import *
import cashdeskapp.urls
import bankapp.urls
import accounts.urls
import enterprise.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('shutdown/', shutdown, name='shutdown'),
    path('caisse/', include(cashdeskapp.urls)),
    path('banque/', include(bankapp.urls)),
    path('account/', include(accounts.urls)),
    path('settings/', include(enterprise.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
