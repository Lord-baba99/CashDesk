from django.db import models

class Enterprise(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to="enterprise/img/logo/")
    description = models.CharField(max_length=255, blank=True, null=True)
    slogan = models.CharField(max_length=255, blank=True, null=True)
    niu = models.CharField(max_length=255, blank=True, null=True)
    rccm = models.CharField(max_length=255, blank=True, null=True)
    rib = models.CharField(max_length=255, blank=True, null=True)
    cnss = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    adress = models.CharField(max_length=255, blank=True, null=True)
    web_site = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
