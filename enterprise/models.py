from django.db import models

class Enterprise(models.Model):
    name = models.CharField(max_length=255, blank=False, null=True)
    logo = models.ImageField(upload_to="enterprise/img/logo/", null=True, blank=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    slogan = models.CharField(max_length=255, blank=True, null=True)
    niu = models.CharField(max_length=255, blank=True, null=True)
    rccm = models.CharField(max_length=255, blank=True, null=True)
    rib = models.CharField(max_length=255, blank=True, null=True)
    cnss = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=False, null=True)
    address = models.CharField(max_length=255, blank=False, null=True)
    web_site = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Exercise(models.Model):
    year = models.CharField(max_length=4, blank=True, null=True)

    def __str__(self):
        return 'Exercice' + self.year

class Month(models.Model):
    is_active = models.BooleanField(default=False, blank=True)
    number = models.IntegerField(default=0)
    name = models.CharField(max_length=20, null=True, blank=True)
    start = models.IntegerField(default=0)
    end = models.IntegerField(default=0)
    year = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

