from django import forms
from .models import *


class BankOperationForm(forms.ModelForm):
	class Meta:
		model = BankOperation
		fields = '__all__'


class BankAccountForm(forms.ModelForm):
	class Meta:
		model = BankAccount
		fields = '__all__'