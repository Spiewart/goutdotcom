from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from . models import PatientProfile

# Create your views here.


class PatientProfileUpdate(LoginRequiredMixin, UpdateView):

    model = PatientProfile
    fields = ["picture"]
