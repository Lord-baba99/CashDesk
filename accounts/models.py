from django.db import models
from django.contrib.auth.models import AbstractUser
from enterprise.models import Enterprise

class Person(AbstractUser, models.Model):
    """
    User account
    """
    SEX_CHOICES = (
        ('homme', 'Homme'), 
        ('Femme', 'femme')
    )

    # personal information
    birthday = models.DateField(null=True, blank=True)
    take_on_date = models.DateField(null=True, blank=True)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='user/profiles/images', null=True, blank=True)
    gender = models.CharField(choices=SEX_CHOICES, default='homme', max_length=10, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    location = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    id_card_number = models.CharField(max_length=100, blank=True, null=True)
    id_card_picture = models.ImageField(upload_to='user/profiles/id_card', blank=True, null=True)
    niu = models.CharField(max_length=100, blank=True, null=True)
    qualification = models.TextField(null=True, blank=True, default=' ')
    comment = models.TextField(null=True, blank=True, default=' ')

    