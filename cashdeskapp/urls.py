from django.urls import path
from . views import *

urlpatterns = [
    path('', cashdesk_home, name='cash-desk-home'),
]