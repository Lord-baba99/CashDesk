from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from urllib.parse import urlencode
from django.urls import reverse
from bankapp.models import *
from cashdeskapp.models import *


def update():
    bank_total_incomes = BankTotalIncome.objects.all()
    bank_total_expenditures = BankTotalExpenditure.objects.all()
    bank_total_operations = BankTotalOperation.objects.all()
    for bank_income in bank_total_incomes:
        bank_income.sum()
    for bank_expenditure in bank_total_expenditures:
        bank_expenditure.sum()
    for bank_operation in bank_total_operations:
        bank_operation.calc()

    if BankReferenceGenerator.objects.all().count() == 0:
        reference = BankReferenceGenerator.objects.create(
            initial='2MC',
            number=1,
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


def init_bank_statistics(month_instance):
    BankDeferrerOperation.objects.create(
        month=month_instance
    ).save()
    BankTotalExpenditure.objects.create(
        month=month_instance
    ).save()
    BankTotalIncome.objects.create(
        month=month_instance
    ).save()
    BankTotalOperation.objects.create(
        month=month_instance
    ).save()
    
    
def init_cashdesk_statistics(month_instance):
    CashDeskDeferrerOperation.objects.create(
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



def initialise(request):
    if request.POST:
        return render(request, 'enterprise/enterprise_config.html')
    return render(request, 'enterprise/welcome.html')


def settings_view(request):
    context = {
        'page_title': 'Parametres'
    }

    return render(request, 'enterprise/settings.html', context)


def create_month(request):
    if request.POST:
        exercise = request.POST.get('year')
        months = Month.objects.filter(year_id=exercise)
        form = MonthForm(request.POST)
        print(request.POST)
        if form.is_valid():
            
            month_number = int(request.POST.get('number'))
            # print(month_number)
            month = Month.objects.get(number=month_number)
            
            if not month.is_active:
                Month.objects.filter(number=month_number).update(is_active=True)
                # month.save()
                init_cashdesk_statistics(month)
                init_bank_statistics(month)
                success_message = f"Le mois de {month.name} a été ajouté avec succès !"
                base_url = reverse("cashdesk-operation-views")
                params = {
                    "current_month": month.id,
                    "exercise": month.year.id
                }
                url = base_url + '?' + '&'.join([f'{key}={value}' for key, value in params.items()])
                return HttpResponse(f"""
                                    <div class="">
                                        <p class="text-green-500 font-medium rounded-lg">{success_message}</p>
                                        <button hx-get="{url}" hx-indicator="#indicator" hx-target="body" hx-swap="innerHTML" class="w-full text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800">
                                        Aller vers  
                                        </button>
                                    </div>
                                    """) #JsonResponse({'success_message': success_message})
            else:
                error_message = f"Le mois de {month.name} existe déjà !"  # Message d'erreur personnalisé
                url = reverse("create-month")
                return HttpResponse(f"""
                                    <div class="">
                                        <p class="text-red-500 font-medium rounded-lg">{error_message}</p>
                                        <button id="form_submit" type="submit" hx-post="{url}" hx-indicator="#indicator" hx-target="#month_responce_message_container" hx-swap="innerHTML" class="w-full text-white bg-indigo-700 hover:bg-indigo-800 focus:ring-4 focus:outline-none focus:ring-indigo-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-indigo-600 dark:hover:bg-indigo-700 dark:focus:ring-indigo-800">Enregistrer</button>
                                    </div>
                                    """) #JsonResponse({'error_message': error_message})
            
        """if not all_ready_exist:
            month_instance = form.save()
            init_statistics(month_instance)
        return HttpResponse(f"Le mois de {month_instance['name']} a été ajouté avec succès !")
        
        else:
            return HttpResponse("Les données saisies sont incorrecte, réessayer !")"""
        """context = {
        'current_month': month_instance.id,
        'exercise': exercise,
        }"""
        error_message = "Les données saisies sont incorrectes, réessayez !"
        url = reverse("create-month")
        return HttpResponse(f"""
                                    <div class="">
                                        <p class="text-red-500 font-medium rounded-lg">{error_message}</p>
                                        <button id="form_submit" type="submit" hx-post="{url}" hx-indicator="#indicator" hx-target="#month_responce_message_container" hx-swap="innerHTML" class="w-full text-white bg-indigo-700 hover:bg-indigo-800 focus:ring-4 focus:outline-none focus:ring-indigo-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-indigo-600 dark:hover:bg-indigo-700 dark:focus:ring-indigo-800">Enregistrer</button>
                                    </div>
                                    """)
    else:
        error_message = "Bad request, request should be post not get, refresh the page and try again. <br>If the proble persite, contact the administrator"
        url = reverse("create-month")
        return HttpResponse(f"""
                                    <div class="">
                                        <p class="text-red-500 font-medium rounded-lg">{error_message}</p>
                                        <button id="form_submit" type="submit" hx-post="{url}" hx-indicator="#indicator" hx-target="#month_responce_message_container" hx-swap="innerHTML" class="w-full text-white bg-indigo-700 hover:bg-indigo-800 focus:ring-4 focus:outline-none focus:ring-indigo-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-indigo-600 dark:hover:bg-indigo-700 dark:focus:ring-indigo-800">Enregistrer</button>
                                    </div>
                                    """)
	# print(context)
    # This block is commented because the initial config process has change.  
    """if request.POST.get('from_cashdesk'):
        url = 'cashdesk-operation-views'
    elif request.POST.get('from_bank'):
        url = 'bank-operation-views'

    query_string = urlencode(context)
    redirect_url = reverse(url) + '?' + query_string
    return HttpResponseRedirect(redirect_url)"""


def create_exercise(request):
	if request.POST:
		exercise = ExerciseForm(request.POST)
		if exercise.is_valid():
			exercises = Exercise.objects.filter(
				year=request.POST.get('year'))
			if exercises.count() > 0:
				context = {
					'error': True,
					'error_message': "L'exercice saisies existe deja !",
					'url': reverse('create-exercise'),
				}
				return render(request, 'enterprise/response/next_step.html', context)
			else:
				exercice_instance = exercise.save()
				if request.POST.get("initialise"):
					post_data = request.POST.dict()
					post_data['year'] = exercice_instance.id
					# print(post_data['year'])
					form = MonthForm(post_data)
						
					if form.is_valid():
						# print("form valid ")
						month_instance = form.save()
						init_cashdesk_statistics(month_instance)
						init_bank_statistics(month_instance)
						name = request.POST['year']
						context = {
							'success': True,
							'success_message': f"L'exercice {name} a été créé avec succès!",
							'name': name,
							'url': reverse('connect-transition')
						}
						return render(request, 'enterprise/response/next_step.html', context)
					else:
						errors_list = {}
						errors = form.errors
						if 'year' in errors:
							errors_list.update(
								{"L'exercice": "L'année est invalide ou vide."})
						if 'name' in errors:
							errors_list.update(
								{'Mois': 'Le premier mois est obligatoire.'})
						if 'start' in errors:
							errors_list.update(
								{"Le debut du mois": "Précisez le premier jour du mois."})
						if 'end' in errors:
							errors_list.update(
								{'La fin du mois': 'Précisez le dernier jour du mois.'})
						# print(errors_list)
						# print('form invalid', request.FILES, ' === ', request.POST)
						# print(errors_list)
						# print(form)
						# print(errors_list)
						context = {
							'form': form,
							'error': True,
							'errors_list': errors_list,
							'error_message': 'Les données saisies ne sont pas correctes !',
							'url': reverse('create-exercise'),
						}
						return render(request, 'enterprise/response/next_step.html', context)
				else: 
					return render(request, '')
	return render(request, 'enterprise/exercise_config.html')


def samples(request):
	return render(request, 'enterprise/user_profile.html')


def create_enterprise(request):
    if request.POST:
        form = EnterpriseForm(request.POST, request.FILES)
        if form.is_valid():
            # print("form valid ")
            form.save()
            name = request.POST['name']
            context = {
                'success': True,
                'success_message': 'a été créé avec succès!',
                'name': name,
                'url': reverse('bank-account-config')
            }
            return render(request, 'enterprise/response/next_step.html', context)
        else:
            errors_list = {}
            errors = form.errors
            if 'logo' in errors:
                errors_list.update(
                    {'Logo': 'Le fichier du logo est invalide ou vide.'})
            if 'name' in errors:
                errors_list.update(
                    {'Nom': 'La raison sociale est obligatoire.'})
            if 'address' in errors:
                errors_list.update({"Adresse": "L'adresse est obligatoire."})
            if 'phone' in errors:
                errors_list.update(
                    {'Téléphone': 'Le numero de téléphone est obligatoire.'})
            # print(errors_list)
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


def connect_transition(request):
    return render(request, 'enterprise/connect.html')
