from enterprise.models import Enterprise

if Enterprise.objects.all().count() > 0:
    enterprise = Enterprise.objects.all().last()
else: enterprise = "unknow"

#print(enterprise)
def global_context(request):
    # Variables de contexte globales
    context = {
        'enterprise': enterprise,
    }
    return context
