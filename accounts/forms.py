from django import forms
from .models import *
from django.contrib.auth.hashers import make_password

class PersonForm(forms.ModelForm):
	class Meta:
		model = Person
		fields = '__all__'
	def clean_password(self):
	    # Récupérer le mot de passe saisi par l'utilisateur
	    password = self.cleaned_data.get('password')
	    # Hacher le mot de passe
	    hashed_password = make_password(password)
	    return hashed_password

class JoinedDate(forms.ModelForm):
	class Meta:
		model = Person
		fields = 'date_joined',