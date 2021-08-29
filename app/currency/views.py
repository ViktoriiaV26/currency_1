from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404

from currency.models import ContactUs, Rate, Source
from currency.forms import SourceForm


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


def source_list(request):
    source = Source.objects.all()
    context = {
        'source_list': source,
    }
    return render(request, 'source_list.html', context=context)


def source_create(request):
    if request.method == 'POST':
        form = SourceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/source/list/')
    elif request.method == 'GET':
        form = SourceForm()
    context = {
        'form': form,
    }
    return render(request, 'source_create.html', context=context)


def source_details(request, source_id):
    # try:
    #     source = Source.objects.get(id=source_id)
    # except Source.DoesNotExist as exc:
    #     raise Http404(exc)
    source = get_object_or_404(Source, id=source_id)

    context = {
        'object': source,
    }
    return render(request, 'source_details.html', context=context)


def source_update(request, source_id):
    source = get_object_or_404(Source, id=source_id)
    if request.method == 'POST':
        form = SourceForm(request.POST, instance=source)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/source/list/')
    elif request.method == 'GET':
        form = SourceForm(instance=source)
    context = {
        'form': form,
    }
    return render(request, 'source_update.html', context=context)


def source_delete(request, source_id):
    source = get_object_or_404(Source, id=source_id)
    if request.method == 'POST':
        source.delete()
        return HttpResponseRedirect('/source/list/')

    context = {
        'object': source,
    }
    return render(request, 'source_delete.html', context=context)
