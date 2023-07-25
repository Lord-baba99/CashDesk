from django.contrib import admin
from .models import *
admin.site.register(CashDesk)
admin.site.register(CashDeskOperation)
admin.site.register(CashDeskReferenceGenerator)
admin.site.register(CashDeskTotalIncome)
admin.site.register(CashDeskTotalExpenditure)
admin.site.register(CashDeskTotalOperation)
admin.site.register(CashDeskDeferrerOperation)
