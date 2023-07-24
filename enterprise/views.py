from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from urllib.parse import urlencode
from django.urls import reverse
from bankapp.models import *

def update():
    bank_total_incomes = BankTotalIncome.objects.all()
    bank_total_expenditures = BankTotalExpenditure.objects.all()
    for bank_total_income in bank_total_incomes:
        bank_total_income.sum()
    for bank_total_expenditure in bank_total_expenditures:
        bank_total_expenditure.sum()

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
				BankTotalExpenditure.objects.create(
					month=Month.objects.last().id
				).save()
				BankTotalIncome.objects.create(
					month=Month.objects.last().id
				).save()
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