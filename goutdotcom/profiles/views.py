from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.views.generic import DetailView, UpdateView
from django.urls import reverse

from .models import PatientProfile

# Create your views here.


class PatientProfileUpdate(LoginRequiredMixin, UpdateView):

    model = PatientProfile
    fields = ['picture', 'date_of_birth', 'age', 'gender', 'race', 'weight', 'height', 'drinks_per_week',]
    def get_success_url(self):
        return self.request.user.get_absolute_url()
