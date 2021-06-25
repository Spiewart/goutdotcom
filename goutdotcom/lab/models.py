from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.fields import NullBooleanField
from django_extensions.db.models import TimeStampedModel
from django.urls import reverse
from django.utils import timezone
from decimal import *

# Create your models here.
def unlogged_user():
    return get_user_model().objects.get_or_create(username='unlogged')[0]

MGDL = 'mg/dL (milligrams per deciliter)'
GDL = 'g/dL (grams per decliter)'
CELLSMM3 = 'cells/mm^3 (cells per cubmic millimeter)'
PLTMICROL = 'PLTS/\u03BCL (platelets per microliter)'
UL = 'U/L (units per liter)'

UNIT_CHOICES = (
    (MGDL, "mg/dL (milligrams per deciliter)"),
    (GDL, "g/dL (grams per decliter)"),
    (CELLSMM3, "cells/mm^3 (cells per cubmic millimeter)"),
    (PLTMICROL, "PLTS/\u03BCL (platelets per microliter)"),
    (UL, "U/L (units per liter)")
)

class Lab(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    value = NullBooleanField()
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True)
    date_drawn = models.DateTimeField(help_text="What day was this lab drawn?", default=timezone.now)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

class Urate(Lab):
    value = models.DecimalField(max_digits=3, decimal_places=1, help_text="Enter the uric acid", null=True, blank=True)
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True, default=MGDL)
    name = "Urate"

    def __str__(self):
        return str(self.value)

    def get_absolute_url(self):
        return reverse("lab:urate-detail", kwargs={"pk":self.pk})

class ALT(Lab):
    value = models.IntegerField(help_text="ALT / SGPT")
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True, default=UL)
    name = "ALT"

    def __str__(self):
        return str(self.value)

    def get_absolute_url(self):
        return reverse("lab:ALT-detail", kwargs={"pk":self.pk})

class AST(Lab):
    value = models.IntegerField(help_text="AST / SGOT")
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True, default=UL)
    name = "AST"

    def __str__(self):
        return str(self.value)

    def get_absolute_url(self):
        return reverse("lab:AST-detail", kwargs={"pk":self.pk})

class Platelet(Lab):
    value = models.IntegerField(help_text="PLT / platelets")
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True, default=PLTMICROL)
    name = "platelet"

    def __str__(self):
        return str(self.value)

    def get_absolute_url(self):
        return reverse("lab:platelet-detail", kwargs={"pk":self.pk})

class WBC(Lab):
    value = models.DecimalField(max_digits=3, decimal_places=1, help_text="WBC")
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True, default=CELLSMM3)
    name = "WBC"

    def __str__(self):
        return str(self.value)

    def get_absolute_url(self):
        return reverse("lab:WBC-detail", kwargs={"pk":self.pk})

class Hemoglobin(Lab):
    value = models.DecimalField(max_digits=3, decimal_places=1, help_text="HGB")
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True, default=GDL)
    name = "hemoglobin"

    def __str__(self):
        return str(self.value)

    def get_absolute_url(self):
        return reverse("lab:hemoglobin-detail", kwargs={"pk":self.pk})

class Creatinine(Lab):
    value = models.DecimalField(max_digits=4, decimal_places=2, help_text="creatinine")
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True, default=MGDL)
    name = "creatinine"

    def eGFR_calculator(self):
        kappa = 0
        alpha = 0

        def sex_vars_kappa(self):
            if self.user.patientprofile.gender == 'male':
                return Decimal(0.9)
            elif self.user.patientprofile.gender == 'female':
                return Decimal(0.7)
            else:
                return False

        def sex_vars_alpha(self):
            if self.user.patientprofile.gender == 'male':
                return Decimal(float(-0.411))
            elif self.user.patientprofile.gender == 'female':
                return Decimal(-0.329)
            else:
                return False

        kappa = sex_vars_kappa(self)
        alpha = sex_vars_alpha(self)

        def race_modifier(self):
            if self.user.patientprofile.race == 'black':
                return Decimal(1.159)
            elif self.user.patientprofile.race == 'white' or self.user.patientprofile.race == 'asian' or self.user.patientprofile.race == 'native american' or self.user.patientprofile.race == 'hispanic':
                return Decimal(1.00)
            else:
                return False

        def sex_modifier(self):
            if self.user.patientprofile.gender == 'male':
                return Decimal(1.018)
            elif self.user.patientprofile.gender == 'female' or self.user.patientprofile.gender == 'non-binary':
                return Decimal(1.00)
            else:
                return False

        if race_modifier(self) != False:
            if sex_modifier(self) != False:
                race_modifier(self)
                sex_modifier(self)
                eGFR = Decimal(141) * min(self.value / kappa, Decimal(1.00)) * max(self.value / kappa, Decimal(1.00)) ** Decimal(-1.209) * Decimal(0.993) ** self.user.patientprofile.get_age() ** race_modifier(self) ** sex_modifier(self)
                return eGFR
            else:
                return "Something went wrong with eGFR calculation"
        else:
            return "Something went wrong with eGFR calculation"

    def __str__(self):
        return (str(self.value) + " " + str(self.created) + " " + "GFR: " + str(self.eGFR_calculator()))

    def get_absolute_url(self):
        return reverse("lab:creatinine-detail", kwargs={"pk":self.pk})
