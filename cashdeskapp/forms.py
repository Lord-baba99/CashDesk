from django import forms
from .models import *

class CashDeskOperationForm(forms.ModelForm):
	class Meta:
		model = CashDeskOperation
		fields = '__all__'