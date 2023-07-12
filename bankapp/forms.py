from django import forms
from .models import *

class BankOperationForm(forms.ModelForm):
	class Meta:
		model = BankOperation
		fields = '__all__'