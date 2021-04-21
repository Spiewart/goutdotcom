from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.views.generic import CreateView, UpdateView
from django.urls import reverse

from .models import PatientProfile

# Create your views here.
class PatientProfileCreate(LoginRequiredMixin, CreateView):

    model = PatientProfile
    fields = ['picture', 'date_of_birth', 'age', 'gender', 'race', 'weight', 'height', 'drinks_per_week',]
    template_name = "profiles/patientprofile_createform.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.user.get_absolute_url()

class PatientProfileUpdate(LoginRequiredMixin, UpdateView):

    model = PatientProfile
    fields = ['picture', 'date_of_birth', 'age', 'gender', 'race', 'weight', 'height', 'drinks_per_week',]
    def get_success_url(self):
        return self.request.user.get_absolute_url()
