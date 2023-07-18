from django.db import models
from accounts.models import Person
from django.urls import reverse
from enterprise.models import *


class BankAccount(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    rib = models.CharField(max_length=255, null=True, blank=True)
    agence = models.CharField(max_length=255, null=True, blank=True)
    reference = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name + ' << ' + self.reference + ' >>'

class BankOperation(models.Model):
    month = models.ForeignKey(Month, on_delete=models.DO_NOTHING)
    bank = models.ForeignKey(BankAccount, on_delete=models.DO_NOTHING)
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
        return reverse('bank-operation-detail', kwargs={"pk": self.pk})

