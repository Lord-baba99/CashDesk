from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from enterprise.models import Exercise


# @login_required(redirect_field_name="bank-home")
def bank_home(request):

    # getting the first month as default for operation views
    month = Month.objects.first()
    if month:
        f_month = month
    else:
        f_month = 'aucun'

    # getting all exercise
    exercises = Exercise.objects.all()

    context = {
        'page_title': 'Banque',
        'exercises': exercises,
        'banks': BankAccount.objects.all(),
        'f_month': f_month,
    }
    return render(request, 'bank/bankhome.html', context)

def search_bank_operation(request):
    if request.method == 'POST':
        target = request.POST.get('search')
        operations = BankOperation.objects.filter(wording__contains=target)
        context = {'operations': operations}
        return render(request, 'bank/bank_operation_search.html', context)

def bank_operation_views(request, month=None, exercise=None):
    """
    Show up all bank operations according to months and years
    param: month = str --> the default month
    param: year = int --> the current year
    """
    # getting the current month to show up the operations view
    c_month = month

    if request.POST:
        c_month_id = request.POST.get('c_month_id')
        c_month = Month.objects.filter(id=c_month_id)
    print(c_month)
    context = {
    'page_title': 'Opérations bancaires',
    'operations': BankOperation.objects.filter(month__name__icontains=c_month, month__year=exercise),
    'banks': BankAccount.objects.all(),
    'exercise': Exercise.objects.get(id=exercise),
    'months': Month.objects.filter(year_id=exercise),
    'current_month': c_month,
    }
    print(context['current_month'])
    return render(request, 'bank/bank_operation.html', context)

# @login_required(redirect_field_name="bank-operation-detail")
def bank_operation_detail(request, pk):
    operation = BankOperation.objects.get(pk=pk)
    context = {
        "operation": operation,
        "page_title": f"Piece de banque : {operation.reference}"
    }
    return render(request, 'bank_operation_detail.html', context)

# @login_required(redirect_field_name="add-bank-operation")
from .forms import BankOperationForm

def add_bank_operation(request):
    if request.method == 'POST':
        form = BankOperationForm(request.POST)
        print(form)
        if form.is_valid():
            print('form valid')
            # Les données du formulaire sont valides
            # Récupérer les valeurs des champs du formulaire
            month = form.cleaned_data['month']
            bank = form.cleaned_data['bank']
            user = form.cleaned_data['user']
            reference = form.cleaned_data['reference']
            wording = form.cleaned_data['wording']
            done_date = form.cleaned_data['done_date']
            expenditure = form.cleaned_data['expenditure']
            income = form.cleaned_data['income']
            amount_digit = form.cleaned_data['amount_digit']
            amount_letter = form.cleaned_data['amount_letter']
            depositor = form.cleaned_data['depositor']
            withdrawer = form.cleaned_data['withdrawer']
            # Traitez les autres champs du formulaire

            if income:
                print('income')
            # Créer l'objet BankOperation avec les données du formulaire
                operation = BankOperation.objects.create(
                    month=month,
                    bank=bank,
                    user=user,
                    reference=reference,
                    wording=wording,
                    done_date=done_date,
                    income=income,
                    amount_digit=amount_digit,
                    amount_letter=amount_letter,
                    depositor=depositor,
                )
                # Enregistrer l'objet BankOperation dans la base de données
                operation.save()

            elif expenditure:
                print('expenditure')
                operation = BankOperation.objects.create(
                    month=month,
                    bank=bank,
                    user=user,
                    reference=reference,
                    wording=wording,
                    done_date=done_date,
                    expenditure=expenditure,
                    amount_digit=amount_digit,
                    amount_letter=amount_letter,
                    withdrawer=withdrawer,
                )

                # Enregistrer l'objet BankOperation dans la base de données
                operation.save()

            # Rediriger ou afficher un message de succès
            if request.POST.get('modal'):
                operations = BankOperation.objects.all()
                context = {
                    'success': 'Formulaire enregistré avec succès !',
                    'page_title': 'Opération bancaire',
                    'banks': BankAccount.objects.all(),
                    'operations': operations,
                }
                return render(request, 'bank/bank_operation.html', context)
            
        else:
            print('form invalid')
            operations = BankOperation.objects.all()
            context = {
                'Error': 'Formulaire invalide !',
                'page_title': 'Opération bancaire',
                'banks': BankAccount.objects.all(),
                'operations': operations,
            }
            return redirect('bank-operation-views', month=request.POST.get('month'), exercise=request.POST.get('exercise'))
    else:
        form = BankOperationForm()

    context = {
        'page_title': 'Opération bancaire',
        'form': form,
        'banks': BankAccount.objects.all()
    }
    return render(request, 'bank/add_bank_operation.html', context)

def get_bank_operation(request, pk=None):
        operation = get_object_or_404(BankOperation, pk=pk)
        print(operation.wording)
        context = {
        'operation': operation,
        }
        return render(request, 'bank/update_bank_operation.html', context)
def update_bank_operation(request):
    if request.POST:
        pk = request.POST.get('pk')
        from_table = request.POST.get('from_table')
        wording = request.POST.get('wording')
        print(f'pk: {pk}, from_table: {from_table}, wording: {wording}')
        operation = BankOperation.objects.get(pk=pk)
        operation.wording = request.POST.get('wording')
        operation.save(update_fields=["wording"])
        context = {
        'operation': operation
        }
        return render(request, 'bank/row_bank.html', context)
    else:
        return redirect('bank-home')

def return_bank_row(request, pk):
    operation = BankOperation.objects.get(pk=pk)
    context = {
    'operation': operation
    }
    return render(request, 'bank/row_bank.html', context)



def add_continue_bank_operation(request):
    bank_op = BankOperationForm
    print(request.POST)
    if request.POST:
        form = bank_op(request.POST)
        print(form)
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