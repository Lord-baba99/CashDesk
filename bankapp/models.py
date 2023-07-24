from django.db import models
from accounts.models import Person
from django.urls import reverse
from enterprise.models import *
from datetime import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver


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


class ReferenceGenerator(models.Model):
    initial = models.CharField(max_length=6)
    number = models.IntegerField(default=0)
    date = models.DateTimeField(default=datetime.now)
    date_str = models.CharField(max_length=6, blank=True, null=True)
    ending_letter = models.CharField(max_length=3)
    full_name = models.CharField(max_length=255, null=True, blank=True)

    def name_formator(self):
        date_obj = datetime.strptime(str(self.date)[:10], "%Y-%m-%d")
        date_formatted = date_obj.strftime("%d%m%y")
        self.date_str = date_formatted
        self.full_name = f'{self.initial}-{self.number}{self.date_str}-{self.ending_letter}'

    def _incrementor(self):
        if ReferenceGenerator.objects.count() > 0:
            old = ReferenceGenerator.objects.last()
            old_number = old.number
            self.number = old_number + 1

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.name_formator()
        self._incrementor()  # Ajouter des parenthèses ici pour appeler la méthode
        super().save(*args, **kwargs)

@receiver(pre_save, sender=ReferenceGenerator)
def pre_save_reference_generator(sender, instance, **kwargs):
    instance.name_formator()

# statitistic

class BankTotalExpenditure(models.Model):
    month_amount = models.BigIntegerField(default=0)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)

    def sum(self):
        operations = BankOperation.objects.filter(month_id=self.month, expenditure=True)
        total = 0
        for operation in operations:
            total += operation.expenditure_amount
        self.month_amount = total

    def __str__(self):
        return f'Total dépense {self.month}'

class BankTotalIncome(models.Model):
    month_amount = models.BigIntegerField(default=0)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)

    def sum(self):
        operations = BankOperation.objects.filter(month_id=self.month, income=True)
        total = 0
        for operation in operations:
            total += operation.income_amount
        self.month_amount = total

    def __str__(self):
        return f'Total récette {self.month}'
