from django.shortcuts import render, redirect
from enterprise.models import Enterprise

def home(request):
	if Enterprise.objects.all().count() < 1:
		return redirect('initialise')
	else:
		return render(request, 'index.html')