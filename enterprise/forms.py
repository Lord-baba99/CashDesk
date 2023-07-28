from django import forms
from .models import *

class MonthForm(forms.ModelForm):
	class Meta:
		model = Month
		fields = '__all__'

class ExerciseForm(forms.ModelForm):
	class Meta:
		model = Exercise
		fields = '__all__'

class EnterpriseForm(forms.ModelForm):
	class Meta:
		model = Enterprise
		fields = '__all__'