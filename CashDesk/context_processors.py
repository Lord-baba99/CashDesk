from enterprise.models import Enterprise

enterprise = Enterprise.objects.all().last()


_global_context = {}


def update_global_context_variable(enterprise):
    global _global_context
    _global_context["enterprise"] = enterprise


def global_context(request):
    enterprise = _global_context.get("enterprise")
    print(enterprise)
    context = {
        "enterprise": enterprise,
    }
    return context
