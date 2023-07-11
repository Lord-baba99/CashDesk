from django.shortcuts import render

def bank_home(request):
	return render(request, 'bank/bankhome.html')