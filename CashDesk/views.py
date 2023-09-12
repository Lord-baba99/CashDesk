from django.shortcuts import render, redirect
from enterprise.models import Enterprise
from CashDesk.settings import COMPRESS_ENABLED

def home(request):
	if Enterprise.objects.all().count() < 1:
		return redirect('initialise')
	else:
		context = {'dev': COMPRESS_ENABLED}
		return render(request, 'index.html')