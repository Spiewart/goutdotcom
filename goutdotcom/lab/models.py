from datetime import datetime, timedelta, timezone
from decimal import *

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel

from ..lab.choices import BOOL_CHOICES, CELLSMM3, GDL, MGDL, PLTMICROL, UL, UNIT_CHOICES
from ..profiles.models import PatientProfile


class Lab(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    ultplan = models.ForeignKey("ultplan.ULTPlan", on_delete=models.SET_NULL, null=True, blank=True, default=None)
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True)
    name = "lab"
    date_drawn = models.DateField(help_text="What day was this lab drawn?", default=None, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name} {self.value} {self.units}"

    def get_absolute_url(self):
        return reverse("lab:detail", kwargs={"pk": self.pk, "lab": self.name})

    def __unicode__(self):
        return self.name

    def user_has_profile(self):
        has_profile = False
        try:
            has_profile = self.user.patientprofile is not None
        except PatientProfile.DoesNotExist:
            pass
        return has_profile


class Urate(Lab):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    value = models.DecimalField(
        max_digits=3, decimal_places=1, help_text="Uric acid is typically reported in micrograms per deciliter (mg/dL)"
    )
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True, default=MGDL)
    name = "urate"


class ALT(Lab):
    value = models.IntegerField(help_text="ALT (SGPT) is typically reported in units per liter (U/L)")
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True, default=UL)
    name = "ALT"


class AST(Lab):
    value = models.IntegerField(help_text="AST (SGOT) is typically reported in units per liter (U/L)")
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True, default=UL)
    name = "AST"


class Platelet(Lab):
    value = models.IntegerField(
        help_text="PLT (platelets) is typically reported in platelets per microliter (PLT/microL)"
    )
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True, default=PLTMICROL)
    name = "platelet"


class WBC(Lab):
    value = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        help_text="WBC (white blood cells) is typically reported as cells per cubic millimeter (cells/mm^3)",
    )
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True, default=CELLSMM3)
    name = "WBC"


class Hemoglobin(Lab):
    value = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        help_text="HGB (hemoglobin) is typically reporeted in grams per deciliter (g/dL)",
    )
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True, default=GDL)
    name = "hemoglobin"


def round_decimal(value, places):
    if value is not None:
        # see https://docs.python.org/2/library/decimal.html#decimal.Decimal.quantize for options
        return value.quantize(Decimal(10) ** -places)
    return value


class Creatinine(Lab):
    value = models.DecimalField(
        max_digits=4, decimal_places=2, help_text="Creatinine is typically reported as milligrams per deciliter (mg/dL)"
    )
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True, default=MGDL)
    name = "creatinine"

    def sex_vars_kappa(self):
        if self.user.patientprofile.gender == "male":
            return Decimal(0.9)
        elif self.user.patientprofile.gender == "female":
            return Decimal(0.7)
        else:
            return False

    def sex_vars_alpha(self):
        if self.user.patientprofile.gender == "male":
            return Decimal(-0.411)
        elif self.user.patientprofile.gender == "female":
            return Decimal(-0.329)
        else:
            return False

    def race_modifier(self):
        if self.user.patientprofile.race == "black":
            return Decimal(1.159)
        elif (
            self.user.patientprofile.race == "white"
            or self.user.patientprofile.race == "asian"
            or self.user.patientprofile.race == "native american"
            or self.user.patientprofile.race == "hispanic"
        ):
            return Decimal(1.00)
        else:
            return False

    def sex_modifier(self):
        if self.user.patientprofile.gender == "male":
            return Decimal(1.018)
        elif self.user.patientprofile.gender == "female" or self.user.patientprofile.gender == "non-binary":
            return Decimal(1.00)
        else:
            return False

    def eGFR_calculator(self):
        if self.user_has_profile() == True:
            if self.user.patientprofile.gender == "non-binary":
                return "Need biologic sex to calculate eGFR"
            else:
                kappa = self.sex_vars_kappa()
                alpha = self.sex_vars_alpha()
                if self.race_modifier() != False:
                    if self.sex_modifier() != False:
                        self.race_modifier()
                        self.sex_modifier()
                        eGFR = (
                            Decimal(141)
                            * min(self.value / kappa, Decimal(1.00)) ** alpha
                            * max(self.value / kappa, Decimal(1.00)) ** Decimal(-1.209)
                            * Decimal(0.993) ** self.user.patientprofile.get_age()
                            * self.race_modifier()
                            * self.sex_modifier()
                        )
                        return round_decimal(eGFR, 2)
                    else:
                        return "Something went wrong with eGFR calculation"
                else:
                    return "Something went wrong with eGFR calculation"
        return "Can't calculate eGFR without an age (make a profile)"

class LabCheck(TimeStampedModel):
    """Model to coordinate labs for monitoring ULTPlan titration."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Need to use alternative nomenclature for referencing ULTPlan model to avoid circular imports
    ultplan = models.ForeignKey("ultplan.ULTPlan", on_delete=models.CASCADE)
    # Related labs
    alt = models.OneToOneField(ALT, on_delete=models.CASCADE, null=True, blank=True, default=None)
    ast = models.OneToOneField(AST, on_delete=models.CASCADE, null=True, blank=True, default=None)
    creatinine = models.OneToOneField(Creatinine, on_delete=models.CASCADE, null=True, blank=True, default=None)
    hemoglobin = models.OneToOneField(Hemoglobin, on_delete=models.CASCADE, null=True, blank=True, default=None)
    platelet = models.OneToOneField(Platelet, on_delete=models.CASCADE, null=True, blank=True, default=None)
    wbc = models.OneToOneField(WBC, on_delete=models.CASCADE, null=True, blank=True, default=None)
    urate = models.OneToOneField(Urate, on_delete=models.CASCADE, null=True, blank=True, default=None)

    due = models.DateField(
        help_text="When is this lab check due?",
        default=(datetime.today().date() + timedelta(days=42)),
    )
    completed = models.BooleanField(choices=BOOL_CHOICES, help_text="Is this lab check completed?", default=False)
    completed_date = models.DateField(
        help_text="When was this lab check completed?",
        blank=True,
        null=True,
        default=None,
    )

    def overdue(self):
        if datetime.today().date() >= self.due:
            return True
        elif datetime.today().date() < self.due:
            return False

    def __str__(self):
        if self.completed == True:
            return f"{str(self.user).capitalize()}'s lab check completed {self.completed_date}"
        else:
            return f"{str(self.user).capitalize()}'s lab check due {self.due}"

    def get_absolute_url(self):
        return reverse("ultplan:detail", kwargs={"pk": self.ultplan.pk})
