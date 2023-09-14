from django.shortcuts import render, redirect
from enterprise.models import Enterprise
from CashDesk.settings import COMPRESS_ENABLED
import subprocess


def home(request):
	if Enterprise.objects.all().count() < 1:
		return redirect('initialise')
	else:
		context = {'dev': COMPRESS_ENABLED}
		return render(request, 'index.html')

def shutdown(request):
    script = '..\kill_server.py'
    if request.POST:
        subprocess.call(script, shell=True)
        return HttpResponse()
