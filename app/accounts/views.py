from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, CreateView

from accounts.forms import SignUpForm
from accounts.models import User


class MyProfileView(LoginRequiredMixin, UpdateView):
    queryset = User.objects.all()
    fields = (
        'first_name',
        'last_name',
    )
    success_url = reverse_lazy('index')
    template_name = 'my_profile.html'

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(id=self.request.user.id)
    #     return queryset
    def get_object(self, queryset=None):
        return self.request.user


class SignUpView(CreateView):
    model = User
    template_name = 'sign_up.html'
    success_url = reverse_lazy('index')
    form_class = SignUpForm


# TODO
# class ActivateUserView(UpdateView):
class ActivateUserView(View):
    pass
    # pattern_name = 'index'
    #
    # def get_redirect_url(self, *args, **kwargs):
    #     username = kwargs.pop('username')
    #     user = get_object_or_404(User, username=username, is_active=False)
    #
    #     user.is_active = True
    #
    #     # update_fields - save only needed(minimum) fields
    #     user.save(update_fields=('is_active',))
    #
    #     messages.info(self.request, 'Your Account is activated!')
    #
    #     return super().get_redirect_url(*args, **kwargs)
