from django.db import models


class ContactUs(models.Model):
    email_from = models.EmailField(max_length=50)
    subject = models.CharField(max_length=250)
    message = models.CharField(max_length=2050)
