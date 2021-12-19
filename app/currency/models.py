from django.db import models
from django.templatetags.static import static

from currency import model_choices as mch


class ContactUs(models.Model):
    email_from = models.EmailField(max_length=50)
    subject = models.CharField(max_length=250)
    message = models.CharField(max_length=2050)


class Source(models.Model):
    source_url = models.URLField(max_length=255)
    name = models.CharField(max_length=64)
    code_name = models.CharField(max_length=25, unique=True, editable=False)

    logo = models.FileField(
        upload_to='sources/logo',
        blank=True,
        null=True,
        default=None,
    )

    def get_logo(self):
        if self.logo:
            return self.logo.url
        return static('images/source-default.jpeg')


class Rate(models.Model):
    sale = models.DecimalField(max_digits=5, decimal_places=2)
    buy = models.DecimalField(max_digits=5, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    source = models.ForeignKey(
        Source,
        related_name='rates',
        on_delete=models.CASCADE,
    )
    type = models.CharField(    # noqa
        max_length=3,
        choices=mch.RATE_TYPE,
        blank=False,
        null=False,
    )


class ResponseLog(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    status_code = models.PositiveSmallIntegerField()
    path = models.CharField(max_length=255)
    response_time = models.PositiveSmallIntegerField(
        help_text='in milliseconds.'
    )
    request_method = models.CharField(max_length=10, choices=mch.REQUEST_METHOD)
