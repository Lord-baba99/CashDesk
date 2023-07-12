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
    bank = models.ForeignKey(BankAccount, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    reference = models.CharField(max_length=20, null=True)
    wording = models.CharField(max_length=255, null=True, blank=True)
    expenditure = models.BooleanField(default=False)
    income = models.BooleanField(default=False)
    done_date = models.DateField()
    create_date = models.DateTimeField(auto_now=True)
    update = models.DateTimeField(auto_now_add=True)
    amount_digit = models.BigIntegerField(default=0)
    amount_letter = models.CharField(max_length=255, null=True, blank=True)
    depositor = models.CharField(max_length=255, null=True, blank=True)
    withdrawer = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.reference

    def get_absolute_url(self):
        return reverse('bank-operation-detail', kwargs={"pk": self.pk})


class CashDeskOperation(models.Model):
    cash_desk = models.ForeignKey(CashDesk, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    reference = models.CharField(max_length=20, null=True)
    wording = models.CharField(max_length=255, null=True, blank=True)
    expenditure = models.BooleanField(default=False)
    income = models.BooleanField(default=False)
    done_date = models.DateField()
    create_date = models.DateTimeField(auto_now=True)
    update = models.DateTimeField(auto_now_add=True)
    amount_digit = models.BigIntegerField(default=0)
    amount_letter = models.CharField(max_length=255, null=True, blank=True)
    depositor = models.CharField(max_length=255, null=True, blank=True)
    withdrawer = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.reference

    def get_absolute_url(self):
        return reverse('', kwargs={"pk": self.pk})


class Mouth(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    start = models.IntegerField(default=0)
    end = models.IntegerField(default=0)
    bank_operation = models.ManyToManyField(BankOperation, related_name='mouth_bank')
    cash_desk_operation = models.ManyToManyField(CashDeskOperation, related_name='mouth_cash')

    def __str__(self):
        return self.name

class Exercice(models.Model):
    year = models.CharField(max_length=4, blank=True, null=True)
    mouths = models.ManyToManyField(Mouth)

    def __str__(self):
        return 'Exercice' + self.year