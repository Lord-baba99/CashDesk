from django.shortcuts import render, redirect
from .forms import *
from .models import *

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
		else:
			print("form is invalid")
	return redirect('bank-operation-views', month=month, exercise=exercise)
