from django import forms
from .models import *

class PersonForm(forms.ModelForm):
	class Meta:
		model = Person
		fields = '__all__'

class JoinedDate(forms.ModelForm):
	class Meta:
		model = Person
		fields = 'date_joined',