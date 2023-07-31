from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from enterprise.models import *
from enterprise.views import update
from urllib.parse import urlencode
from django.urls import reverse
from .forms import BankOperationForm
from .models import *

# @login_required(redirect_field_name="bank-home")
def bank_home(request):
    update()
    # getting the last month as default for operation views
    month = Month.objects.last()
    if month:
        f_month = month
    else:
        f_month = 0

    # getting all exercise
    exercises = Exercise.objects.all()

    context = {
        'page_title': 'Banque',
        'exercises': exercises,
        'banks': BankAccount.objects.all(),
        'f_month': f_month,
    }
    return render(request, 'bank/bankhome.html', context)

def search_bank_operation(request, month=None, exercise=None):
    update()
    if request.method == 'POST':
        target = request.POST.get('search')
        operations = BankOperation.objects.filter(wording__contains=target, month__year=exercise, month_id=month)
        context = {
        'operations': operations, 
        'current_month': Month.objects.get(pk=month),
        'exercise': Exercise.objects.get(pk=exercise)
        }
        return render(request, 'bank/bank_operation_search.html', context)

def bank_operation_views(request, **kwargs):
    """
    Show up all bank operations according to months and years
    param: month = str --> the default month
    param: year = int --> the current year
    """
    update()
    # getting the current month to show up the operations view
    
    if request.POST:
        month = request.POST.get('current_month')
        exercise = request.POST.get('exercise')
        target = request.POST.get('search')
        
        operations = BankOperation.objects.filter(wording__contains=target, month__year=exercise, month_id=month)
        context = {
        'operations': operations, 
        'current_month': Month.objects.get(pk=month).id,
        'exercise': Exercise.objects.get(pk=exercise),
        }
        return render(request, 'bank/search_bank_operation.html', context)

    else:
        month = request.GET.get('current_month')
        exercise = request.GET.get('exercise')
        # print('mois ', month)
        if month:
            c_month = Month.objects.get(id=month)
            operations = BankOperation.objects.filter(month_id=c_month.id, month__year=exercise)
            try:
                total_expenditure = BankTotalExpenditure.objects.get(month=month).month_amount
            except BankTotalExpenditure.DoesNotExist:
                total_expenditure = 0

            try:
                total_income = BankTotalIncome.objects.get(month=month).month_amount
            except BankTotalIncome.DoesNotExist:
                total_income = 0
            try:
                total_operation = BankTotalOperation.objects.get(month=month).month_amount
            except BankTotalOperation.DoesNotExist:
                total_operation = 0
            try:
                deferrer = BankDeferrerOperation.objects.get(month=month).initial
            except BankDeferrerOperation.DoesNotExist:
                deferrer = 0

            # print('total depense :', total_expenditure)
            # print(c_month.id,' c_month')

            context = {
            'page_title': 'Opérations bancaires',
            'operations': operations,
            'banks': BankAccount.objects.all(),
            'exercise': Exercise.objects.get(id=exercise),
            'months': Month.objects.filter(year_id=exercise),
            'current_month': c_month.id,
            'month_name': c_month.name,
            'reference': BankReferenceGenerator.objects.last(),
            'total_expenditure': total_expenditure,
            'total_income': total_income,
            'total_operation': total_operation,
            'deferrer': deferrer,
            }
            return render(request, 'bank/bank_operation_table.html', context)

        if Month.objects.all().count()<1:
            current_month = 0
        else:
            current_month = Month.objects.all().last()
        
        context = {
        'page_title': 'Opérations bancaires',
        'exercise': Exercise.objects.get(id=exercise),
        'current_month': current_month,
        }
        return render(request, 'bank/bank_operation_table.html', context)

# @login_required(redirect_field_name="bank-operation-detail")
def bank_operation_detail(request, pk):
    operation = BankOperation.objects.get(pk=pk)
    # print('month :', request.GET.get('month'), ' exercise :', request.GET.get('exercise'))
    context = {
        "operation": operation,
        "page_title": f"Piece de banque : {operation.reference}",
        "month": request.GET.get('month'),
        "exercise": request.GET.get('exercise'),
    }
    return render(request, 'bank/bank_operation_detail.html', context)

# @login_required(redirect_field_name="add-bank-operation")
def add_bank_operation(request, month=None, year=None):

    if request.method == 'POST':
        form = BankOperationForm(request.POST)
        # print(request.POST)
        # print(form)
        if form.is_valid():
            # print('form valid')
            form.save()
            reference = BankReferenceGenerator.objects.create(
                initial='2MC',
                ending_letter='B'
                )
            # print('before save ', reference)
            # print('after save ', reference)
            if request.POST.get('modal'):
                                
                context = {
                    'current_month': request.POST.get('month'),
                    'exercise': request.POST.get('exercise'),
                    'success': 'Formulaire enregistré avec succès !'
                }
                # print(request.POST.get('exercise'), request.POST.get('month'))
                query_string = urlencode(context)
                redirect_url = reverse('bank-operation-views') + '?' + query_string
                # print(redirect_url)
                return HttpResponseRedirect(redirect_url)
            
        else:
            # print('form invalid')
            operations = BankOperation.objects.all()
            context = {
                'Error': 'Formulaire invalide !',
                'page_title': 'Opération bancaire',
                'exercise': request.POST.get('exercise'),
                'current_month': request.POST.get('month'),
            }

            query_string = urlencode(context)
            redirect_url = reverse('bank-operation-views') + '?' + query_string
            return HttpResponseRedirect(redirect_url)
        

def add_bank_operation_views(request, month, year):
    form = BankOperationForm()

    context = {
        'page_title': 'Opération bancaire',
        'form': form,
        'banks': BankAccount.objects.all(),
        'current_month': Month.objects.get(pk=month),
        'exercise': Exercise.objects.get(pk=year),
    }
    return render(request, 'bank/add_bank_operation.html', context)

def get_bank_operation(request, pk=None, month=None, exercise=None):
        operation = get_object_or_404(BankOperation, pk=pk)
        # print(operation.wording)
        context = {
        'operation': operation,
        'current_month': month,
        'exercise': exercise,
        }
        # print(exercise, 'exercise get-bank')
        return render(request, 'bank/update_bank_operation.html', context)

def delete_bank_operation(request, month=None, exercise=None, pk=None):
    operation = BankOperation.objects.get(pk=pk)
    if operation:
        operation.delete()

    context = {
        'current_month': month,
        'exercise': exercise,
        'action': f"L'operation {operation} a été supprimée avec succès !",
    }
    query_string = urlencode(context)
    redirect_url = reverse('bank-operation-views') + '?' + query_string
    return HttpResponseRedirect(redirect_url)

def update_bank_operation(request):
    if request.POST:
        pk = request.POST.get('pk')
        from_table = request.POST.get('from_table')
        wording = request.POST.get('wording')
        # print(f'pk: {pk}, from_table: {from_table}, wording: {wording}')
        operation = BankOperation.objects.get(pk=pk)
        operation.wording = request.POST.get('wording')
        operation.save(update_fields=["wording"])
        context = {
        'operation': operation,
        'current_month': request.POST.get('current_month'),
        'exercise': request.POST.get('exercise'),
        }
        # print(request.POST.get('current_month'), 'current_month')
        return render(request, 'bank/row_bank.html', context)
    else:
        return redirect('bank-operation-views')

def return_bank_row(request, pk, month=None, exercise=None):
    operation = BankOperation.objects.get(pk=pk)
    context = {
    'operation': operation,
    'current_month': month,
    'exercise': exercise,

    }
    return render(request, 'bank/row_bank.html', context)



def add_continue_bank_operation(request):
    bank_op = BankOperationForm
    # print(request.POST)
    if request.POST:
        form = bank_op(request.POST)
        # print(form)
        if form.is_valid():
            form.save()
            context = {
                'page_title': 'Opération bancaire',
                'form': bank_op,
            }
            return render(request, 'bank-operation.html', context)

# @login_required(redirect_field_name="delete-multiple-bank-operation")
def delete_multiple_bank_operation(request):
    if request.POST:
        for name in request.POST:
            pk = name[0]
            bank_operation = BankOperation.objects.get(pk=pk)
            bank_operation.delete()
        return redirect('bank-home')


def add_bank_account(request):
    if request.POST:
        pass

def bank_account_config(request):
    if request.POST:
        form = BankAccountFormSet(request.POST)
        if form.is_valid():
            # print('valid')
            context = {
            'success': True,
            'success_message': 'Succès !',
            'url': reverse('cashdesk-config')
            }
            return render(request, 'enterprise/response/next_step.html', context)
        else:
            errors_list = form.errors
            context = {
            'form': form,
            'error': True,
            'errors_list': errors_list,
            'error_message': 'Les données saisies ne sont pas correctes !',
            'url': reverse('bank-account-config'),
            }
            return render(request, 'enterprise/response/next_step.html', context)

    context = {
    'enterprise': Enterprise.objects.all().first(),
    'formset': BankAccountFormSet(),
    'form_number': 0,
    }
    return render(request, 'bank/bank_account_config.html', context)

def add_bank_form(request):
    if request.POST:
        form_number = request.POST.get('form_number')

        context = {
        'form_number': int(form_number) + 1,
        "bank_order": int(request.POST.get('form-TOTAL_FORMS')) + 1
        }
        return render(request, 'bank/bank_account.html', context)

    else:
        return HttpResponse('The request must be POST !')