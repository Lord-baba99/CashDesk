from django.urls import path
from . views import bank_home

urlpatterns = [
	path('', bank_home, name='bank-home')
]