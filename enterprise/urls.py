from django.urls import path
from .views import *

urlpatterns = [
	path('create-month/<int:exercise>/<int:month>', create_month, name='create-month'),
]