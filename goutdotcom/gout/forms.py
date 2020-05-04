from django import forms
from django.forms import ModelForm
from gout.models import Flare, Patient, Info, Urate, Creatinine

class CreatePatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'age', 'gender', 'mrn', 'email', 'owner']
