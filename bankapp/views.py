from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *

@login_required(redirect_field_name="treasury-home")
def home(request):
    context = {
        'page_title': 'Accueil'
    }
    return render(request, "treasury_home.html", context)

@login_required(redirect_field_name="bank-home")
def bank(request):
    operations = BankOperation.objects.all()
    context = {
        'page_title': 'Opérations bancaires',
        'operations': operations,
    }
    return render(request, 'bank.html', context)

@login_required(redirect_field_name="bank-operation-detail")
def bank_operation_detail(request, pk):
    operation = BankOperation.objects.get(pk=pk)
    context = {
        "operation": operation,
        "page_title": f"Piece de banque : {operation.reference}"
    }
    return render(request, 'bank_operation_detail.html', context)

@login_required(redirect_field_name="add-bank-operation")
def add_bank_operation(request):
    bank_op = BankOperationForm
    print(request.POST)
    if request.POST:
        form = bank_op(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('bank-home')
    context = {
        'page_title': 'Opération bancaire',
        'form': bank_op,
        'banks': BankAccount.objects.all()
    }
    return render(request, 'bank-operation.html', context)

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

@login_required(redirect_field_name="delete-multiple-bank-operation")
def delete_multiple_bank_operation(request):
    if request.POST:
        for name in request.POST:
            pk = name[0]
            bank_operation = BankOperation.objects.get(pk=pk)
            bank_operation.delete()
        return redirect('bank-home')