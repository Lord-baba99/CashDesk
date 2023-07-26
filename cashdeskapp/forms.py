from django import forms
from .models import *

class CashDeskOperationForm(forms.ModelForm):
	class Meta:
		model = CashDeskOperation
		fields = '__all__'


class CashDeskForm(forms.ModelForm):
	class Meta:
		model = CashDesk
		fields = '__all__'