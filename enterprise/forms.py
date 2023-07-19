from django import forms
from .models import *

class MonthForm(forms.ModelForm):
	class Meta:
		model = Month
		fields = '__all__'