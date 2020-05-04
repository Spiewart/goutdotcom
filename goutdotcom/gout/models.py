from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime

# Create your models here.
class Patient(models.Model):
    first_name = models.CharField(max_length=128, help_text='Enter first name')
    last_name = models.CharField(max_length=128, help_text='Enter last name')
    age = models.IntegerField(range(1-150), help_text='Enter age')

    sexes = (('male', 'male'), ('female', 'female'))

    gender = models.CharField(max_length=6, choices=sexes, help_text='Enter gender')
    mrn = models.IntegerField(primary_key=True, help_text='Enter MRN')
    email = models.EmailField()

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    #owner_group = models.ForeignKey(User.Group, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def provider_or_not(self):
        if self.owner == 'testuser':
            return True
        else:
            return False

    class Meta:
        ordering = ['last_name', 'first_name']
        permissions = (("can_create_new_patient", "Creates new patient"),)

    def __str__(self):
        return f'{str(self.last_name), str(self.first_name)}'

    def get_absolute_url(self):
        return reverse('patient_detail', args=[str(self.mrn)])

class Flare(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    date = models.DateField()

    joints = (('Toe', 'Toe'), ('Ankle', 'Ankle'), ('Knee', 'Knee'), ('Hip', 'Hip'), ('Finger', 'Finger'), ('Wrist', 'Wrist'), ('Elbow','Elbow'), ('Shoulder', 'Shoulder'))
    location = models.CharField(max_length=8, choices=joints, default='Toe', help_text="What joint did the flare occur in?")

    treatments = (('NSAID', 'NSAID'), ('colchicine', 'colchicine'), ('PO steroid', 'PO steroid'), ('INJ steroid', 'INJ steroid'), ('Tincture of time', 'Tincture of time'))
    treated_with = models.CharField(max_length=20, choices=treatments, default='NSAID', help_text="What was the flare treated with?")

    duration = models.IntegerField(help_text="How long did it last? (days)")
    urate_at_flare = models.DecimalField(max_digits=3, decimal_places=1, help_text="What was the uric acid at the time of the flare?")

    class Meta:
        ordering = ['patient']

    def __str__(self):
        return f'{(str(self.date), str(self.patient), str(self.location))}'

    def get_absolute_url(self):
        return reverse('flare-detail', args=[str(self.date)])

class Urate(models.Model):
    uric_acid = models.DecimalField(max_digits=3, decimal_places=1, help_text="uric acid?")
    date = models.DateField(auto_now=True)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.uric_acid)

class Creatinine(models.Model):
    creatinine = models.DecimalField(max_digits=4, decimal_places=2, help_text="creatinine")
    date = models.DateField(auto_now=True)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)

    def eGFR_calculator(self):
        kappa = 0
        alpha = 0
        def sex_vars(self):
            if patient.gender == 'male':
                kappa = 0.9
                alpha = -0.411
            elif patient.gender == 'female':
                kappa = 0.7
                alpha = -0.329
            else:
                return "Can't calculate eGFR without gender."
        def race_modifier(self):
            if patient.race == 'black':
                return 1.159
            else:
                return 1
        def sex_modifier(self):
            if patient.gender == 'female':
                return 1.018
            else:
                return 1

        eGFR = 141 * min(self.creatinine / kappa, 1) * max(self.creatinine / kappa, 1) ** -1.209 * 0.993 ** patient.age ** race_modifier() ** sex_modifier()

    def __str__(self):
        return str(self.creatinine)

class Info(models.Model):
    urate = models.FloatField()
    creatinine = models.FloatField()
    BMI = models.IntegerField()
    drinks_per_week = models.IntegerField()
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.urate} {self.patient}'
