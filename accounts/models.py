from django.db import models

# Create your models here.
class Contact(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    countryName = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)

class ContactDetails(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    countryName = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)