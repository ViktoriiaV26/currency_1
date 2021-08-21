from django.http import HttpResponse
from currency.models import ContactUs


def hello_world(request):
    return HttpResponse('Hello World')


def contactus_list(request):
    contact = ContactUs.objects.all()
    result = []
    for c in contact:
        result.append(
            f'Id: {c.id} Email: {c.email_from} Subject: {c.subject} Message: {c.message}</br>'
        )

    return HttpResponse(str(result))
