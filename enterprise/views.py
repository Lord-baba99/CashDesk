from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from urllib.parse import urlencode
from django.urls import reverse

def settings_view(request):
	context = {
		'page_title': 'Parametres'
	}

	return render(request, 'enterprise/settings.html', context)

def create_month(request, month=None, exercise=None):
	if request.POST:
		months = Month.objects.filter(year_id=exercise)
		print(months)
		form = MonthForm(request.POST)
		if form.is_valid():
			all_ready_exist = False
			for x in months:
				if request.POST.get('name').lower() in x.name.lower():
					all_ready_exist = True
			if not all_ready_exist:
				form.save()
		else:
			print("form is invalid")

	context = {
		'current_month':month,
		'exercise':exercise,
	}

	print(context)
	query_string = urlencode(context)
	redirect_url = reverse('bank-operation-views') + '?' + query_string
	return HttpResponseRedirect(redirect_url)

def samples(request):
	return render(request, 'enterprise/user_profile.html')