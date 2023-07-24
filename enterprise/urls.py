from django.urls import path
from .views import *

urlpatterns = [
	path('', settings_view, name='settings-view'),
	path('samples', samples, name='samples'),
	path('create-month/<int:exercise>/', create_month, name='create-month'),
]