from django.db.models import Avg, Max, Min, Sum

def operations_chart_data(year, months, operations):
    """
    Operations chart.
    Warning: year and operations should be a model instance of respectivly exercise and operation
    """
    last_year = year.objects.first().id
    expenditure = operations.objects.filter(
        month__year=last_year, expenditure=True
    )
    incomes = operations.objects.filter(
        month__year=last_year, income=True
    )
    months = months.objects.filter(year_id=last_year)
    expenditures_data = []
    incomes_data = []
    months_data = []
    
    for month in months:
        expenditures_avg = operations.objects.filter(
            expenditure=True, month_id=month.id
        ).aggregate(Avg("expenditure_amount"))["expenditure_amount__avg"]
        incomes_avg = operations.objects.filter(
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
    
    return {"exp": expenditures_data, "inc": incomes_data, "mon": months_data}
