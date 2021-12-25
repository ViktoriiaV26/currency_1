from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.conf import settings
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView

from currency.models import ContactUs, Rate, Source
from currency.forms import SourceForm, RateForm
from django.core.mail import send_mail
from currency.services import get_latest_rates


class ContactUsListView(ListView):
    queryset = ContactUs.objects.all()
    template_name = 'contactus_list.html'


class ContactUsCreateView(CreateView):
    model = ContactUs
    queryset = Source.objects.all()
    success_url = reverse_lazy('currency:contactus-list')
    template_name = 'contactus_create.html'
    fields = (
        'email_from',
        'subject',
        'message',
    )

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        email_from = form.cleaned_data['email_from']

        full_email_message = f"""
        Email From: {email_from}
        Message: {message}
        """

        send_mail(
            subject,
            full_email_message,
            settings.EMAIL_HOST_USER,
            [settings.SUPPORT_EMAIL],
            fail_silently=False,
        )
        return super().form_valid(form)


class RateListView(ListView):
    queryset = Rate.objects.all().select_related('source').order_by('-created')
    template_name = 'rate_list.html'


class RateCreateView(CreateView):
    queryset = Rate.objects.all()
    form_class = RateForm
    success_url = reverse_lazy('currency:rate-list')
    template_name = 'rate_create.html'


class RateDetailView(LoginRequiredMixin, DetailView):
    queryset = Rate.objects.all()
    template_name = 'rate_details.html'


class RateUpdateView(UserPassesTestMixin, UpdateView):
    queryset = Rate.objects.all()
    form_class = RateForm
    success_url = reverse_lazy('currency:rate-list')
    template_name = 'rate_update.html'

    def test_func(self):
        return self.request.user.is_superuser


class RateDeleteView(UserPassesTestMixin, DeleteView):
    queryset = Rate.objects.all()
    success_url = reverse_lazy('currency:rate-list')
    template_name = 'rate_delete.html'

    def test_func(self):
        return self.request.user.is_superuser


class SourceListView(ListView):
    queryset = Source.objects.all()
    template_name = 'source_list.html'


class SourceCreateView(CreateView):
    queryset = Source.objects.all()
    form_class = SourceForm
    success_url = reverse_lazy('currency:source-list')
    template_name = 'source_create.html'


class SourceDetailView(DetailView):
    queryset = Source.objects.all()
    template_name = 'source_details.html'


class SourceUpdateView(UpdateView):
    queryset = Source.objects.all()
    form_class = SourceForm
    success_url = reverse_lazy('currency:source-list')
    template_name = 'source_update.html'


class SourceDeleteView(DeleteView):
    queryset = Source.objects.all()
    success_url = reverse_lazy('currency:source-list')
    template_name = 'source_delete.html'


class LatestRateView(TemplateView):
    template_name = 'latest_rates.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rate_list'] = get_latest_rates()
        return context
