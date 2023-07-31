from django import forms
from .models import *
from django.forms import formset_factory


class CashDeskOperationForm(forms.ModelForm):
	class Meta:
		model = CashDeskOperation
		fields = '__all__'


class CashDeskForm(forms.ModelForm):
	class Meta:
		model = CashDesk
		fields = '__all__'

CashDeskFormSet = formset_factory(CashDeskForm)