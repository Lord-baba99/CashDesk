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

def create_exercise(request):
	if request.POST:
		if request.POST.get("initialise"):
			exercise = ExerciseForm(request.POST)
			if exercise.is_valid():
				exercises = Exercise.objects.filter(year=request.POST.get('year'))
				if exercises.count() > 0:
					context = {
					'error': True,
					'error_message': "L'exercice saisies existe deja !",
					'url': reverse('create-exercise'),
					}
					return render(request, 'enterprise/response/next_step.html', context)
				else:
					# exercise.save()
					pass
			post_data = request.POST.dict()
			post_data['year'] = Exercise.objects.all().last().id
			print(post_data['year'])
			form = MonthForm(post_data)
		else:
			pass
			

		if form.is_valid():
			print("form valid ")
			# form.save()
			name = request.POST['year']
			context = {
			'success': True,
			'success_message': f"L'exercice {name} a été créé avec succès!",
			'name': name,
			'url': reverse('signup')
			}
			return render(request, 'enterprise/response/next_step.html', context)
		else:
			errors_list = {}
			errors = form.errors
			if 'year' in errors:
				errors_list.update({"L'exercice": "L'année est invalide ou vide."})
			if 'name' in errors:
				errors_list.update({'Mois': 'Le premier mois est obligatoire.'})
			if 'start' in errors:
				errors_list.update({"Le debut du mois": "Précisez le premier jour du mois."})
			if 'end' in errors:
				errors_list.update({'La fin du mois': 'Précisez le dernier jour du mois.'})
			# print(errors_list)
			# print('form invalid', request.FILES, ' === ', request.POST)
			# print(errors_list)
			print(form)
			print(errors_list)
			context = {
			'form': form,
			'error': True,
			'errors_list': errors_list,
			'error_message': 'Les données saisies ne sont pas correctes !',
			'url': reverse('create-exercise'),
			}
			return render(request, 'enterprise/response/next_step.html', context)
	return render(request, 'enterprise/exercise_config.html')

def samples(request):
	return render(request, 'enterprise/user_profile.html')

def create_enterprise(request):
	if request.POST:
		form = EnterpriseForm(request.POST, request.FILES)
		if form.is_valid():
			# print("form valid ")
			# form.save()
			name = request.POST['name']
			context = {
			'success': True,
			'success_message': 'a été créé avec succès!',
			'name': name,
			'url': reverse('create-exercise')
			}
			return render(request, 'enterprise/response/next_step.html', context)
		else:
			errors_list = {}
			errors = form.errors
			if 'logo' in errors:
				errors_list.update({'Logo': 'Le fichier du logo est invalide ou vide.'})
			if 'name' in errors:
				errors_list.update({'Nom': 'La raison sociale est obligatoire.'})
			if 'address' in errors:
				errors_list.update({"Adresse": "L'adresse est obligatoire."})
			if 'phone' in errors:
				errors_list.update({'Téléphone': 'Le numero de téléphone est obligatoire.'})
			print(errors_list)
			# print('form invalid', request.FILES, ' === ', request.POST)
			# print(errors_list)
			context = {
			'form': form,
			'error': True,
			'errors_list': errors_list,
			'error_message': 'Les données saisies ne sont pas correctes !',
			'url': reverse('create-enterprise'),
			}
			return render(request, 'enterprise/response/next_step.html', context)
	return render(request, 'enterprise/exercise_config.html')