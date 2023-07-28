from django.urls import path
from .views import *

urlpatterns = [
	path('', settings_view, name='settings-view'),
	path('samples', samples, name='samples'),
	path('welcome', initialise, name='initialise'),
	path('create-month/<int:exercise>/', create_month, name='create-month'),
	path('create-enterprise/', create_enterprise, name='create-enterprise'),
	path('create-exercise/', create_exercise, name='create-exercise'),
]