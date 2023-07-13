from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *

# @login_required(redirect_field_name="treasury-home")
def home(request):
    context = {
        'page_title': 'Accueil'
    }
    return render(request, "treasury_home.html", context)

# @login_required(redirect_field_name="bank-home")
def bank_home(request):
    operations = BankOperation.objects.all()
    print(request.user)
    context = {
        'page_title': 'Opérations bancaires',
        'operations': operations,
        'banks': BankAccount.objects.all(),
    }
    return render(request, 'bank/bankhome.html', context)

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
        if form.is_valid():
            print('form valid')
            # Les données du formulaire sont valides
            # Récupérer les valeurs des champs du formulaire
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
                return render(request, 'bank/bankhome.html', context)
            else:
                # Rediriger vers une autre page ou afficher un message de succès
                return HttpResponseRedirect('/success-page/')
        else:
            print('form invalid')
    else:
        form = BankOperationForm()

    context = {
        'page_title': 'Opération bancaire',
        'form': form,
        'banks': BankAccount.objects.all()
    }
    return render(request, 'bank/add_bank_operation.html', context)


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