from goutdotcom.profiles.forms import PatientProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from django.views.generic import CreateView, UpdateView
from django.urls import reverse

from .models import PatientProfile

# Create your views here.
class PatientProfileCreate(LoginRequiredMixin, CreateView):
    model = PatientProfile
    form_class = PatientProfileForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.user.get_absolute_url()

class PatientProfileUpdate(LoginRequiredMixin, UpdateView):
    model = PatientProfile
    form_class = PatientProfileForm

    def get_success_url(self):
        return self.request.user.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super(PatientProfileUpdate, self).get_context_data(**kwargs)
        context.update({
            'user': self.request.user
        })
        return context

    def get_object(self, queryset=None):
        model = self.model
        user = self.request.user
        try:
            queryset = model.objects.filter(user=self.request.user)
        except ObjectDoesNotExist:
            raise Http404("No object found matching this query.")

        obj = super(PatientProfileUpdate, self).get_object(queryset=queryset)
        return obj
