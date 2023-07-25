from django.contrib import admin
from .models import *

admin.site.register(BankOperation)
admin.site.register(BankAccount)
admin.site.register(BankReferenceGenerator)
admin.site.register(BankTotalIncome)
admin.site.register(BankTotalExpenditure)
admin.site.register(BankTotalOperation)
admin.site.register(BankDeferrerOperation)
