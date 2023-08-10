from django.db import models


# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)

    age = models.IntegerField(null=True, blank=True)

    gender = models.CharField(max_length=2, null=True, blank=True)

    status = models.CharField(max_length=20, null=True, blank=True)
