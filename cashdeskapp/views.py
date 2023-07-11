from django.shortcuts import render

def cashdesk_home(request):
    context = {
        'page_title': 'Caisse'
    }
    return render(request, 'cashdesk/cashdeskhome.html', context)