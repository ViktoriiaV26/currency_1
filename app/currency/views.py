from django.http import HttpResponse
from django.shortcuts import render

from currency.models import ContactUs, Rate


def hello_world(request):
    return HttpResponse('Hello World')


def index(request):
    return render(request, 'index.html')


def contactus_list(request):
    contact = ContactUs.objects.all()
    context = {
        'contactus_list': contact,
    }
    return render(request, 'contactus_list.html', context=context)


def rate_list(request):
    rates = Rate.objects.all()
    context = {
        'rate_list': rates,
    }
    return render(request, 'rate_list.html', context=context)
