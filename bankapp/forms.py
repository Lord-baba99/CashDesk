from django import forms
from .models import *
from django.forms import formset_factory


class BankOperationForm(forms.ModelForm):
	class Meta:
		model = BankOperation
		fields = '__all__'


class BankAccountForm(forms.ModelForm):
	class Meta:
		model = BankAccount
		fields = '__all__'

BankAccountFormSet = formset_factory(BankAccountForm, extra=2)