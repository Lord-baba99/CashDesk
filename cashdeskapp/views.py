from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from enterprise.models import *
from enterprise.views import update
from urllib.parse import urlencode
from django.urls import reverse
from .forms import CashDeskOperationForm
from .models import *
from django.db.models import Avg, Max, Min, Sum

# @login_required(redirect_field_name="cashdesk-home")


def cashdesk_home(request):
    update()
    # getting the last month as default for operation views
    month = Month.objects.filter(is_active=True).last()
    if month:
        f_month = month
    else:
        f_month = 0

    # getting all exercise
    exercises = Exercise.objects.order_by("-year")

    # chart
    last_exercise = Exercise.objects.first().id
    expenditures = CashDeskOperation.objects.filter(
        month__year=last_exercise, expenditure=True
    )
    incomes = CashDeskOperation.objects.filter(month__year=last_exercise, income=True)
    months = Month.objects.filter(year_id=last_exercise)

    expenditures_data = []
    incomes_data = []
    months_data = []
    for month in months:
        expenditures_avg = CashDeskOperation.objects.filter(
            expenditure=True, month_id=month.id
        ).aggregate(Avg("expenditure_amount"))["expenditure_amount__avg"]
        incomes_avg = CashDeskOperation.objects.filter(
            income=True, month_id=month.id
        ).aggregate(Avg("income_amount"))["income_amount__avg"]
        if expenditures_avg:
            expenditures_data.append(expenditures_avg)
        else:
            expenditures_data.append(0)
        if incomes_avg:
            incomes_data.append(incomes_avg)
        else:
            incomes_data.append(0)
        months_data.append(month.name)

    # print(expenditures_data)
    # print(incomes_data)
    # print(months_data)
    context = {
        "page_title": "Caisse",
        "exercises": exercises,
        "cashdesks": CashDesk.objects.all(),
        "f_month": f_month,
        "expenditures_data": expenditures_data,
        "incomes_data": incomes_data,
        "months_data": months_data,
    }
    return render(request, "cashdesk/cashdeskhome.html", context)


def search_cashdesk_operation(request, month=None, exercise=None):
    update()
    if request.method == "POST":
        target = request.POST.get("search")
        operations = CashDeskOperation.objects.filter(
            wording__contains=target, month__year=exercise, month_id=month
        )
        context = {
            "operations": operations,
            "current_month": Month.objects.get(pk=month),
            "exercise": Exercise.objects.get(pk=exercise),
        }
        return render(request, "cashdesk/cashdesk_operation_search.html", context)


def cashdesk_operation_views(request, **kwargs):
    """
    Show up all cashdesk operations according to months and years
    param: month = str --> the default month
    param: year = int --> the current year
    """
    
    update()
    # getting the current month to show up the operations view
    month = request.GET.get("current_month")
    exercise = request.GET.get("exercise")
    # print(month)

    if request.POST:
        # print(request.POST)
        month = request.POST.get("current_month")
        exercise = request.POST.get("exercise")
        target = request.POST.get("search")
        operations = CashDeskOperation.objects.filter(
            wording__contains=target, month__year=exercise, month_id=month
        ).order_by("done_date")
        context = {
            'operations': operations,
            'current_month': Month.objects.get(pk=month).id,
            'exercise': Exercise.objects.get(pk=exercise),
        }
        return render(request, 'cashdesk/search_cashdesk_operation.html', context)
    else:
        operations = CashDeskOperation.objects.filter(
            month_id=month, month__year=exercise
        ).order_by("done_date")

        # print('mois ', month)

        if month:
            # print(month, "month")
            c_month = Month.objects.get(id=month)
            try:
                total_expenditure = CashDeskTotalExpenditure.objects.get(
                    month=month
                ).month_amount
                # print(total_expenditure, "total expenditure")
            except CashDeskTotalExpenditure.DoesNotExist:
                total_expenditure = 0

            try:
                total_income = CashDeskTotalIncome.objects.get(month=month).month_amount
            except CashDeskTotalIncome.DoesNotExist:
                total_income = 0
            try:
                total_operation = CashDeskTotalOperation.objects.get(
                    month=month
                ).month_amount
            except CashDeskTotalOperation.DoesNotExist:
                total_operation = 0
            try:
                deferrer = CashDeskDeferrerOperation.objects.get(month=month).initial
            except CashDeskDeferrerOperation.DoesNotExist:
                deferrer = 0
        else:
            total_expenditure = 0
            total_income = 0
            total_operation = 0
            deferrer = 0
            # print('total depense :', total_expenditure)
            # print(c_month.id, ' c_month')
        if Month.objects.all().count() < 1:
            c_month = 0
        else:
            c_month = month # Month.objects.all().last().id

        context = {
            "page_title": "Opérations à la caisse",
            "operations": operations,
            "cashdesks": CashDesk.objects.all(),
            "exercise": Exercise.objects.get(id=exercise),
            "months": Month.objects.filter(year_id=exercise).order_by("number"),
            "current_month": c_month,
            "month_name": Month.objects.get(id=c_month).name,
            "reference": CashDeskReferenceGenerator.objects.last(),
            "total_expenditure": total_expenditure,
            "total_income": total_income,
            "total_operation": total_operation,
            "deferrer": deferrer,
        }
        if request.POST:
            return render(request, "cashdesk/search_cashdesk_operation.html", context)
        else:
            return render(request, "cashdesk/cashdesk_operation_table.html", context)


# @login_required(redirect_field_name="cashdesk-operation-detail")


def cashdesk_operation_detail(request, pk):
    operation = CashDeskOperation.objects.get(pk=pk)
    # print('month :', request.GET.get('month'),
    #      ' exercise :', request.GET.get('exercise'))
    context = {
        "operation": operation,
        "page_title": f"Piece de caisse : {operation.reference}",
        "month": request.GET.get("month"),
        "exercise": request.GET.get("exercise"),
    }
    return render(request, "cashdesk/cashdesk_operation_detail.html", context)


# @login_required(redirect_field_name="add-cashdesk-operation")


def add_cashdesk_operation(request, month=None, year=None):

    if request.method == "POST":
        form = CashDeskOperationForm(request.POST)
        # print(request.POST)
        # print(form)
        if form.is_valid():
            # print('form valid')
            form.save()
            reference = CashDeskReferenceGenerator.objects.create(
                initial="2MC", ending_letter="C"
            )
            # print('before save ', reference)
            # print('after save ', reference)
            if request.POST.get("modal"):

                context = {
                    "current_month": request.POST.get("month"),
                    "exercise": request.POST.get("exercise"),
                    "success": "Formulaire enregistré avec succès !",
                }
                # print(request.POST.get('exercise'), request.POST.get('month'))
                query_string = urlencode(context)
                redirect_url = reverse("cashdesk-operation-views") + "?" + query_string
                # print(redirect_url)
                return HttpResponseRedirect(redirect_url)

        else:
            # print('form invalid')
            operations = CashDeskOperation.objects.all().order_by("done_date")
            context = {
                "Error": "Formulaire invalide !",
                "page_title": "Opération bancaire",
                "exercise": request.POST.get("exercise"),
                "current_month": request.POST.get("month"),
            }

            query_string = urlencode(context)
            redirect_url = reverse("cashdesk-operation-views") + "?" + query_string
            return HttpResponseRedirect(redirect_url)


def add_cashdesk_operation_views(request, month, year):
    form = CashDeskOperationForm()

    context = {
        "page_title": "Opération bancaire",
        "form": form,
        "cashdesks": CashDesk.objects.all(),
        "current_month": Month.objects.get(pk=month),
        "exercise": Exercise.objects.get(pk=year),
    }
    return render(request, "cashdesk/add_cashdesk_operation.html", context)


def get_cashdesk_operation(request, pk=None, month=None, exercise=None):
    operation = get_object_or_404(CashDeskOperation, pk=pk)
    # print(operation.wording)
    context = {
        "operation": operation,
        "current_month": month,
        "exercise": exercise,
    }
    # print(exercise, 'exercise get-cashdesk')
    return render(request, "cashdesk/update_cashdesk_operation.html", context)


def delete_cashdesk_operation(request, month=None, exercise=None, pk=None):
    operation = CashDeskOperation.objects.get(pk=pk)
    if operation:
        operation.delete()

    context = {
        "current_month": month,
        "exercise": exercise,
        "action": f"L'operation {operation} a été supprimée avec succès !",
    }
    query_string = urlencode(context)
    redirect_url = reverse("cashdesk-operation-views") + "?" + query_string
    return HttpResponseRedirect(redirect_url)


def update_cashdesk_operation(request):
    if request.POST:
        pk = request.POST.get("pk")
        from_table = request.POST.get("from_table")
        wording = request.POST.get("wording")
        # print(f'pk: {pk}, from_table: {from_table}, wording: {wording}')
        operation = CashDeskOperation.objects.get(pk=pk)
        operation.wording = request.POST.get("wording")
        operation.save(update_fields=["wording"])
        context = {
            "operation": operation,
            "current_month": request.POST.get("current_month"),
            "exercise": request.POST.get("exercise"),
        }
        # print(request.POST.get('current_month'), 'current_month')
        return render(request, "cashdesk/row_cashdesk.html", context)
    else:
        return redirect("cashdesk-operation-views")


def return_cashdesk_row(request, pk, month=None, exercise=None):
    operation = CashDeskOperation.objects.get(pk=pk)
    context = {
        "operation": operation,
        "current_month": month,
        "exercise": exercise,
    }
    return render(request, "cashdesk/row_cashdesk.html", context)


def add_continue_cashdesk_operation(request):
    cashdesk_op = CashDeskOperationForm
    # print(request.POST)
    if request.POST:
        form = cashdesk_op(request.POST)
        # print(form)
        if form.is_valid():
            form.save()
            context = {
                "page_title": "Opération bancaire",
                "form": cashdesk_op,
            }
            return render(request, "cashdesk-operation.html", context)


# @login_required(redirect_field_name="delete-multiple-cashdesk-operation")


def delete_multiple_cashdesk_operation(request):
    if request.POST:
        for name in request.POST:
            pk = name[0]
            cashdesk_operation = CashDeskOperation.objects.get(pk=pk)
            cashdesk_operation.delete()
        return redirect("cashdesk-home")


def add_cashdesk(request):
    pass


def cashdesk_config(request):
    if request.POST:
        form = CashDeskFormSet(request.POST)
        if form.is_valid():
            print("valid")
            for x in form:
                x.save()
            context = {
                "success": True,
                "success_message": "Succès !",
                "url": reverse("create-exercise"),
            }
            return render(request, "enterprise/response/next_step.html", context)
        else:
            errors_list = form.errors
            context = {
                "form": form,
                "error": True,
                "errors_list": errors_list,
                "error_message": "Les données saisies ne sont pas correctes !",
                "url": reverse("cashdesk-config"),
            }
            return render(request, "enterprise/response/next_step.html", context)

    context = {
        "enterprise": Enterprise.objects.all().first(),
        "formset": CashDeskFormSet(),
        "form_number": 0,
    }
    return render(request, "cashdesk/cashdesk_config.html", context)


def add_cashdesk_form(request):
    if request.POST:
        form_number = request.POST.get("form_number")

        context = {
            "form_number": int(form_number) + 1,
            "cashdesk_order": int(request.POST.get("form-TOTAL_FORMS")) + 1,
            "enterprise": Enterprise.objects.all().first(),
        }
        return render(request, "cashdesk/cashdesk.html", context)

    else:
        return HttpResponse("The request must be POST !")
