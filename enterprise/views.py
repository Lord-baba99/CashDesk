from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from urllib.parse import urlencode
from django.urls import reverse
from bankapp.models import *
from cashdeskapp.models import *

def update():
    bank_total_incomes = BankTotalIncome.objects.all()
    bank_total_expenditures = BankTotalExpenditure.objects.all()
    bank_total_operations = BankTotalOperation.objects.all()
    for bank_total_income in bank_total_incomes:
        bank_total_income.sum()
    for bank_total_expenditure in bank_total_expenditures:
        bank_total_expenditure.sum()
    for bank_total_operation in bank_total_operations:
        bank_total_operation.calc()

    if BankReferenceGenerator.objects.all().count() == 0:
        reference = BankReferenceGenerator.objects.create(
				initial='2MC',
				number = 1,
				ending_letter='B'
				)
        reference.save()

    cashdesk_total_incomes = CashDeskTotalIncome.objects.all()
    cashdesk_total_expenditures = CashDeskTotalExpenditure.objects.all()
    cashdesk_total_operations = CashDeskTotalOperation.objects.all()
    for cashdesk_total_income in cashdesk_total_incomes:
        cashdesk_total_income.sum()
    for cashdesk_total_expenditure in cashdesk_total_expenditures:
        cashdesk_total_expenditure.sum()
    for cashdesk_total_operation in cashdesk_total_operations:
        cashdesk_total_operation.calc()

    if CashDeskReferenceGenerator.objects.all().count() == 0:
        reference = CashDeskReferenceGenerator.objects.create(
            initial='2MC',
            number=1,
            ending_letter='C'
        )
        reference.save()

def initialise(request):
	if request.POST:
		return render(request, 'enterprise/enterprise_config.html')
	return render(request, 'enterprise/welcome.html')

def settings_view(request):
	context = {
		'page_title': 'Parametres'
	}

	return render(request, 'enterprise/settings.html', context)

def create_month(request, month=None, exercise=None):
	if request.POST:
		months = Month.objects.filter(year_id=exercise)
		# print(months)
		form = MonthForm(request.POST)
		if form.is_valid():
			all_ready_exist = False
			for x in months:
				if request.POST.get('name').lower() in x.name.lower():
					all_ready_exist = True
			if not all_ready_exist:
				month_instance = form.save()
				BankTotalExpenditure.objects.create(
					month=month_instance
				).save()
				BankTotalIncome.objects.create(
					month=month_instance
				).save()
				BankTotalOperation.objects.create(
					month=month_instance
				).save()
				BankDeferrerOperation.objects.create(
					month=month_instance
				).save()
				CashDeskTotalExpenditure.objects.create(
					month=month_instance
				).save()
				CashDeskTotalIncome.objects.create(
					month=month_instance
				).save()
				CashDeskTotalOperation.objects.create(
					month=month_instance
				).save()
				CashDeskDeferrerOperation.objects.create(
					month=month_instance
				).save()
		else:
			# print("form is invalid")
			pass

	context = {
		'current_month': month_instance.id,
		'exercise': exercise,
	}

	# print(context)
	query_string = urlencode(context)
	redirect_url = reverse('bank-operation-views') + '?' + query_string
	return HttpResponseRedirect(redirect_url)

def create_enterprise(request):
	if request.POST:
		form = EnterpriseForm(request.POST)
		if form.is_valid:
			form.save()
			name = request.POST['name']
			context = {
			'succes': True,
			'sucess_message': f'{name} a bien été créé !',
			}
			return HttpResponse(context)
		else:
			context = {
			'succes': False,
			'error_message': 'Les données saisies ne sont pas correctes !',
			}
			return HttpResponse(context)


def samples(request):
	return render(request, 'enterprise/user_profile.html')