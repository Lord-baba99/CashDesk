from django.contrib import admin
from .models import *

admin.site.register(BankOperation)
admin.site.register(BankAccount)
admin.site.register(ReferenceGenerator)
admin.site.register(BankTotalIncome)
admin.site.register(BankTotalExpenditure)
