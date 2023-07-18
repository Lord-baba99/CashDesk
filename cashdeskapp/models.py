from django.db import models
from accounts.models import Person
from django.urls import reverse
from enterprise.models import *

class CashDesk(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    reference = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.reference

class CashDeskOperation(models.Model):
    month = models.ForeignKey(Month, on_delete=models.DO_NOTHING)
    cash_desk = models.ForeignKey(CashDesk, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    reference = models.CharField(max_length=20, null=True)
    wording = models.CharField(max_length=255, null=True, blank=True)
    expenditure = models.BooleanField(default=False)
    income = models.BooleanField(default=False)
    done_date = models.DateField()
    create_date = models.DateTimeField(auto_now=True)
    update = models.DateTimeField(auto_now_add=True)
    income_amount = models.BigIntegerField(default=0)
    expenditure_amount = models.BigIntegerField(default=0)
    amount_letter = models.CharField(max_length=255, null=True, blank=True)
    depositor = models.CharField(max_length=255, null=True, blank=True)
    withdrawer = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.reference

    def get_absolute_url(self):
        return reverse('', kwargs={"pk": self.pk})


