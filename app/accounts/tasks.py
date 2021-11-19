from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def activate_email(activation_link, email_to):

    subject = 'Activate your account today!'
    body = f'''
    Hello!
    Here is you activation link: {activation_link}
    '''

    send_mail(
        subject,
        body,
        settings.EMAIL_HOST_USER,
        [email_to],
        fail_silently=False,
    )
