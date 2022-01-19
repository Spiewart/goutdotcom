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
    reference_lower = models.IntegerField(default=100, help_text="Lower limit of normal values for Lab")
    reference_upper = models.IntegerField(default=200, help_text="Upper limit of normal values for Lab")
    abnormal_flag = models.BooleanField(
        choices=BOOL_CHOICES, help_text="Is this lab abnormal?", verbose_name="Abnormal Flag", default=False
    )

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

    def lab_abnormal_low(self):
        """
        Function that checks whether a Lab.value is less than the lower limit of normal.

        Returns:
            bool: returns True if Lab.value is less than the lower limit of normal, False if not.
        """
        if self.value < self.reference_lower:
            return True
        else:
            return False

    def lab_abnormal_high(self):
        """
        Function tahat checks whether a Lab.value is greater than the upper limit of normal.

        Returns:
            bool: returns True if Lab.value is greater than the upper limit of normal, False if not.
        """
        if self.value > self.reference_upper:
            return True
        else:
            return False

    def three_x_high(self):
        """
        Function that checks whether a lab value which is greater than the upper limit of normal is greater than 3 times the upper limit of normal.

        Returns:
            bool: returns true if Lab.value is greater than 3 times the upper limit of normal
        """
        if self.value > (3 * self.reference_upper):
            return True
        else:
            return False

    def abnormal_checker(self):
        """
        Function that checks whether or not a Lab.value is abnormal.
        If lab is abnormal, set abnormal_flag attribute to True.

        Returns:
            dictionary or None: Returns a dictionary with descriptors of the Lab.value abnormality if present, otherwise returns None
        """
        abnormalities = {"highorlow": None, "threex": False}

        # Check if lab is lower than reference range
        if self.lab_abnormal_low() == True:
            abnormalities["highorlow"] = "L"
            self.abnormal_flag = True
            return abnormalities
        elif self.lab_abnormal_high() == True:
            abnormalities["highorlow"] = "H"
            self.abnormal_flag = True
            if self.three_x_high() == True:
                abnormalities["threex"] = True
            return abnormalities
        else:
            return None


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
    reference_lower = models.DecimalField(
        max_digits=3, decimal_places=1, default=3.5, help_text="Lower limit of normal values for urate"
    )
    reference_upper = models.DecimalField(
        max_digits=3, decimal_places=1, default=7.2, help_text="Upper limit of normal values for urate"
    )


class ALT(Lab):
    LOWER_LIMIT = 7
    UPPER_LIMIT = 55

    value = models.IntegerField(help_text="ALT (SGPT) is typically reported in units per liter (U/L)")
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True, default=UL)
    name = "ALT"
    reference_lower = models.IntegerField(default=LOWER_LIMIT, help_text="Lower limit of normal values for ALT")
    reference_upper = models.IntegerField(default=UPPER_LIMIT, help_text="Upper limit of normal values for ALT")


class AST(Lab):
    LOWER_LIMIT = 10
    UPPER_LIMIT = 40

    value = models.IntegerField(help_text="AST (SGOT) is typically reported in units per liter (U/L)")
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True, default=UL)
    name = "AST"
    reference_lower = models.IntegerField(default=LOWER_LIMIT, help_text="Lower limit of normal values for AST")
    reference_upper = models.IntegerField(default=UPPER_LIMIT, help_text="Upper limit of normal values for AST")


class Platelet(Lab):
    LOWER_LIMIT = 150
    UPPER_LIMIT = 450

    value = models.IntegerField(
        help_text="PLT (platelets) is typically reported in platelets per microliter (PLT/microL)"
    )
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True, default=PLTMICROL)
    name = "platelet"
    reference_lower = models.IntegerField(default=LOWER_LIMIT, help_text="Lower limit of normal values for platelets")
    reference_upper = models.IntegerField(default=UPPER_LIMIT, help_text="Upper limit of normal values for platelets")


class WBC(Lab):
    LOWER_LIMIT = Decimal(4.5)
    UPPER_LIMIT = Decimal(11.0)

    value = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        help_text="WBC (white blood cells) is typically reported as cells per cubic millimeter (cells/mm^3)",
    )
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True, default=CELLSMM3)
    name = "WBC"
    reference_lower = models.DecimalField(
        max_digits=3, decimal_places=1, default=LOWER_LIMIT, help_text="Lower limit of normal values for WBC"
    )
    reference_upper = models.DecimalField(
        max_digits=3, decimal_places=1, default=UPPER_LIMIT, help_text="Upper limit of normal values for WBC"
    )


class Hemoglobin(Lab):
    LOWER_LIMIT = Decimal(13.5)
    UPPER_LIMIT = Decimal(17.5)

    value = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        help_text="HGB (hemoglobin) is typically reporeted in grams per deciliter (g/dL)",
    )
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True, default=GDL)
    name = "hemoglobin"
    reference_lower = models.DecimalField(
        max_digits=3, decimal_places=1, default=LOWER_LIMIT, help_text="Lower limit of normal values for hemoglobin"
    )
    reference_upper = models.DecimalField(
        max_digits=3, decimal_places=1, default=UPPER_LIMIT, help_text="Upper limit of normal values for hemoglobin"
    )


def round_decimal(value, places):
    if value is not None:
        # see https://docs.python.org/2/library/decimal.html#decimal.Decimal.quantize for options
        return value.quantize(Decimal(10) ** -places)
    return value


class Creatinine(Lab):
    LOWER_LIMIT = Decimal(0.74)
    UPPER_LIMIT = Decimal(1.35)

    value = models.DecimalField(
        max_digits=4, decimal_places=2, help_text="Creatinine is typically reported as milligrams per deciliter (mg/dL)"
    )
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True, default=MGDL)
    name = "creatinine"
    reference_lower = models.DecimalField(
        max_digits=4, decimal_places=2, default=LOWER_LIMIT, help_text="Lower limit of normal values for creatinine"
    )
    reference_upper = models.DecimalField(
        max_digits=4, decimal_places=2, default=UPPER_LIMIT, help_text="Upper limit of normal values for creatinine"
    )

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
    # Related model LabCheck in the event a LabCheck with abnormal labs needs F/U Labs
    abnormal_labcheck = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, default=None)
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

    def check_completed_labs(self):
        """
        Function that checks all the labs in a completed LabCheck.
        Adds the return dictionary from abnormal_checker() method to a new dictionary abnormal_labs for returning to views and templates.

        returns: dictionary of dictionaries containing information on abnormal labs
        """
        # Create empty dictionary of abnormal labs
        abnormal_labs = {}
        # Call abnormal_checker() for each Lab in completed LabCheck
        if self.alt.abnormal_checker():
            abnormal_labs["alt"] = self.alt.abnormal_checker()
        if self.ast.abnormal_checker():
            abnormal_labs["ast"] = self.ast.abnormal_checker()
        if self.creatinine.abnormal_checker():
            abnormal_labs["creatinine"] = self.creatinine.abnormal_checker()
        if self.hemoglobin.abnormal_checker():
            abnormal_labs["hemoglobin"] = self.hemoglobin.abnormal_checker()
        if self.platelet.abnormal_checker():
            abnormal_labs["platelet"] = self.platelet.abnormal_checker()
        if self.wbc.abnormal_checker():
            abnormal_labs["wbc"] = self.wbc.abnormal_checker()
        if self.urate.abnormal_checker():
            abnormal_labs["urate"] = self.urate.abnormal_checker()
        # Return abnormal_labs dictionary with subdictionaries for each abnormal lab
        return abnormal_labs

    def __str__(self):
        if self.completed == True:
            return f"{str(self.user).capitalize()}'s lab check completed {self.completed_date}"
        else:
            return f"{str(self.user).capitalize()}'s lab check due {self.due}"

    def get_absolute_url(self):
        return reverse("ultplan:detail", kwargs={"pk": self.ultplan.pk})
