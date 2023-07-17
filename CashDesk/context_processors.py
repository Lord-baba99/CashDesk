from enterprise.models import Enterprise

if Enterprise.objects.all().count() > 0:
    enterprise = Enterprise.objects.get(id=1)
else: enterprise = "unknow"

def global_context(request):
    # Variables de contexte globales
    context = {
        'enterprise': enterprise,
        'variable2': 'Valeur 2',
        # ...
    }
    return context
