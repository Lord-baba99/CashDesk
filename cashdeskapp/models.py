from django.db.models import Avg, Max, Min, Sum
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from datetime import datetime
from django.db import models
from accounts.models import Person
from django.urls import reverse
from enterprise.models import *

class CashDesk(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.DO_NOTHING)
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
        return reverse('cashdesk-operation-detail', kwargs={"pk": self.pk})



class CashDeskReferenceGenerator(models.Model):
    initial = models.CharField(max_length=6)
    number = models.IntegerField(default=0)
    date = models.DateTimeField(default=datetime.now)
    date_str = models.CharField(max_length=6, blank=True, null=True)
    ending_letter = models.CharField(max_length=3)
    full_name = models.CharField(max_length=255, null=True, blank=True)

    def _incrementor(self):
        if CashDeskReferenceGenerator.objects.count() > 0:
            old = CashDeskReferenceGenerator.objects.last()
            old_number = old.number
            # print('nombre initial :', self.number)
            # print('ancien nombre :', old_number)
            self.number = old_number + 1
            # print('nombre final :', self.number)

    def name_formator(self):
        date_obj = datetime.strptime(str(self.date)[:10], "%Y-%m-%d")
        date_formatted = date_obj.strftime("%d%m%y")
        self.date_str = date_formatted
        self.full_name = f'{self.initial}-{self.number}{self.date_str}-{self.ending_letter}'

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self._incrementor()
        self.name_formator()
        super().save(*args, **kwargs)

# @receiver(pre_save, sender=CashDeskReferenceGenerator)
# def pre_save_reference_generator(sender, instance, **kwargs):
#     instance.name_formator()

# statitistic


class CashDeskTotalExpenditure(models.Model):
    month_amount = models.BigIntegerField(default=0)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)

    def sum(self):
        operations = CashDeskOperation.objects.filter(
            month_id=self.month, expenditure=True)
        amount_sum = operations.aggregate(Sum('expenditure_amount'))
        if amount_sum['expenditure_amount__sum']:
            self.month_amount = amount_sum['expenditure_amount__sum']
            self.save()
        else:
            self.month_amount = 0
            self.save()

    def __str__(self):
        return f'Total dépense {self.month}'


class CashDeskTotalIncome(models.Model):
    month_amount = models.BigIntegerField(default=0)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)

    def sum(self):
        operations = CashDeskOperation.objects.filter(
            month_id=self.month, income=True)
        amount_sum = operations.aggregate(Sum('income_amount'))
        if amount_sum['income_amount__sum']:
            self.month_amount = amount_sum['income_amount__sum']
            self.save()
        else:
            self.month_amount = 0
            self.save()

    def __str__(self):
        return f'Total récette {self.month}'


class CashDeskDeferrerOperation(models.Model):
    month_amount = models.BigIntegerField(default=0)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    initial = models.BigIntegerField(default=0)
    finall = models.BigIntegerField(default=0)

    def initialise(self):
        try:
            month_before = Month.objects.filter(id__lt=self.month.number).last()
        except Month.DoesNotExist:
            month_before = None
        # print(month_before)
        if month_before:
            defer_before = CashDeskDeferrerOperation.objects.get(
                month_id=month_before.id)
            # print(defer_before.finall)
            self.initial = defer_before.finall

    def update_finall(self, total):
        self.finall = total
        self.save()

    def save(self, *args, **kwargs):
        self.initialise()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Report du mois de {self.month}'

# Signal post_save pour mettre à jour CashDeskDeferrerOperation lorsque CashDeskTotalOperation est enregistrée ou mise à jour


@receiver(post_save, sender='cashdeskapp.CashDeskTotalOperation')
def update_cashdesk_deferrer_operation(sender, instance, **kwargs):
    try:
        cashdesk_deferrer_operation = CashDeskDeferrerOperation.objects.get(
            month_id=instance.month_id)
        total = instance.month_amount
        cashdesk_deferrer_operation.update_finall(total)
    except CashDeskDeferrerOperation.DoesNotExist:
        pass


class CashDeskTotalOperation(models.Model):
    month_amount = models.BigIntegerField(default=0)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)

    def calc(self):
        defer = CashDeskDeferrerOperation.objects.get(month_id=self.month).initial
        total_income = CashDeskTotalIncome.objects.get(
            month_id=self.month).month_amount
        total_expenditure = CashDeskTotalExpenditure.objects.get(
            month_id=self.month).month_amount
        # print('(model) total depense ', total_income)
        result = defer + total_income - total_expenditure
        self.month_amount = result
        self.save()

    def __str__(self):
        return f'Total solde du mois de {self.month}'
