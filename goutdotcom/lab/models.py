from datetime import datetime, timedelta, timezone
from decimal import *

from django.conf import settings
from django.db import models, transaction
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
    baseline = models.BooleanField(
        choices=BOOL_CHOICES, help_text="Is this the baseline for this User?", verbose_name="Baseline", default=False
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
        Function that checks whether a Lab.value is greater than the upper limit of normal.

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

    def var_x_high(self, var, baseline=None):
        """
        Function that checks whether a Lab value is high.
        Takes optional argument baseline.
        Var argument is a percentage (110%, 120%, etc.) to base the comparson by.

        Returns:
            bool: returns true if Lab.value is greater than var times the upper limit of normal or baseline if supplied.
        """
        # Check if baseline argument provided, use that for comparison
        if self.baseline:
            if self.value > (var * baseline):
                return True
            else:
                return False
        # Else use reference_upper for comparison
        else:
            if self.value > (var * self.reference_upper):
                return True
            else:
                return False

    def var_x_low(self, var, baseline=None):
        """
        Function that checks whether a Lab value is low.
        Takes optional argument baseline.
        Var argument is a percentage (90%, 80%, etc.) to base the comparson by.

        Returns:
            bool: returns true if Lab.value is lower than var times the lower limit of normal
        """
        if self.baseline:
            if self.value < (var * baseline):
                return True
            else:
                return False
        else:
            if self.value < (var * self.reference_lower):
                return True
            else:
                return False

    def var_x_baseline_high(self, var, baseline):
        """Function evaluated if a lab value is greater than var % of its baseline

        Args:
            var (Float): Float percentage for calculating where the current Lab value is relative to baseline
            baseline (Lab.value): Lab value argument for comparing the current Lab value to.
        Returns:
            bool: True if Lab.value is > var * baseline, False if not
        """
        if self.value > (baseline * var):
            return True
        else:
            return False

    def var_x_baseline_low(self, var, baseline):
        """Function evaluated if a lab value is less than var % of its baseline
        Args:
            var (Float): Float percentage for calculating where the current Lab value is relative to baseline
            baseline (Lab.value): Lab value argument for comparing the current Lab value to.
        Returns:
            bool: True if Lab.value is < var * baseline, False if not
        """
        if self.value < (baseline * var):
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

    # Overwriting save() method to check if baseline is set to True, marks all others as False if so
    # Makes baseline unique for the model class for the User
    def save(self, *args, **kwargs):
        if not self.baseline:
            return super(ALT, self).save(*args, **kwargs)
        with transaction.atomic():
            ALT.objects.filter(user=self.user, baseline=True).update(baseline=False)
            return super(ALT, self).save(*args, **kwargs)


class AST(Lab):
    LOWER_LIMIT = 10
    UPPER_LIMIT = 40

    value = models.IntegerField(help_text="AST (SGOT) is typically reported in units per liter (U/L)")
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True, default=UL)
    name = "AST"
    reference_lower = models.IntegerField(default=LOWER_LIMIT, help_text="Lower limit of normal values for AST")
    reference_upper = models.IntegerField(default=UPPER_LIMIT, help_text="Upper limit of normal values for AST")

    # Overwriting save() method to check if baseline is set to True, marks all others as False if so
    # Makes baseline unique for the model class for the User
    def save(self, *args, **kwargs):
        if not self.baseline:
            return super(AST, self).save(*args, **kwargs)
        with transaction.atomic():
            AST.objects.filter(user=self.user, baseline=True).update(baseline=False)
            return super(AST, self).save(*args, **kwargs)


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

    # Overwriting save() method to check if baseline is set to True, marks all others as False if so
    # Makes baseline unique for the model class for the User
    def save(self, *args, **kwargs):
        if not self.baseline:
            return super(Platelet, self).save(*args, **kwargs)
        with transaction.atomic():
            Platelet.objects.filter(user=self.user, baseline=True).update(baseline=False)
            return super(Platelet, self).save(*args, **kwargs)

    def get_baseline(self):
        """Method that fetches the User's baseline Platelet value.
        Returns baseline Platelet value if so.
        Else returns None.
        """
        try:
            self.baseline = Platelet.objects.filter(user=self.user).get(baseline=True).value
        except:
            self.baseline = None
        return self.baseline

    def abnormal_high(self, labcheck, labchecks):
        """Function that processes a high Platelet.
        Takes a LabCheck and list of LabChecks as argument, the latter to avoid hitting the database multiple times with several different labs.

        Args:
            labcheck ([LabCheck]): [LabCheck the Platelet is related to.]
            labchecks ([List]): [List of LabChecks provided by the function processing the abnormal Platelet.]

        Returns:
            string or nothing: returns "urgent" if urgent LabCheck follow up required, nonurgent if non-urgent required
        """
        # Check if labcheck is a follow up on an abnormal_labcheck
        if labcheck.abnormal_labcheck:
            # Check if abnormal_labcheck was for a high Platelet value
            if labcheck.abnormal_labcheck.platelet.abnormal_checker().get("highorlow") == "H":
                # Check if first LabCheck Lab was normal or low
                ### NEED TO CHECK HOW FAR BACK FIRST LABCHECK WAS, SIMILAR TO CREATININE WHICH ISN'T WORKING
                if (
                    labchecks[len(labchecks) - 1].platelet.abnormal_checker() == None
                    or labchecks[len(labchecks) - 1].platelet.abnormal_checker().get("highorlow") == "L"
                ):
                    # If Platelet value is > 1.5x times the upper limit of normal (will be second in a row), raise urgent flag
                    # Will discontinue ULT and PPx, pause ULTPlan
                    if labcheck.platelet.var_x_high(1.5):
                        return "urgent"
                    else:
                        return None
                # Check if Platelet values are always high by:
                # Average the list of all platelet values
                # Check if average is greater than 1.1x the upper limit of normal (~500K)
                # Return None if so to ignore the high value
                elif len(labchecks) > 3:
                    platelet_list = []
                    for labcheck in labchecks:
                        platelet_list.append(labcheck.platelet.value)
                    if sum(platelet_list) / len(platelet_list) > (self.reference_upper * 1.1):
                        return None
                # If first LabCheck was high, flag nonurgent and will eventually get triggered as always high
                else:
                    return "nonurgent"
            else:
                # LabCheck must be for follow up of a low Platelet value
                # If Platelet value is 1.5x the upper limit of normal (> 675K), raise nonurgent flag
                if labcheck.platelet.var_x_high(1.5):
                    return "nonurgent"
        else:
            # LabCheck is not follow up for another abnormal_labcheck
            # If Platelet value is 1.5x the upper limit of normal (> 675K), raise nonurgent flag
            if labcheck.platelet.var_x_high(1.5):
                return "nonurgent"

    def abnormal_low(self, labcheck, labchecks):
        """Function that processes a low Platelet.
        Takes a LabCheck and list of LabChecks as argument, the latter to avoid hitting the database multiple times with several different labs.

        Args:
            labcheck ([LabCheck]): [LabCheck the Platelet is related to.]
            labchecks ([List]): [List of LabChecks provided by the function processing the abnormal Platelet.]

        Returns:
            string or nothing: returns "urgent" if urgent LabCheck follow up required, nonurgent if non-urgent required
        """
        # Check if labcheck is a follow up on an abnormal_labcheck
        if labcheck.abnormal_labcheck:
            # Check if abnormal_labcheck was for a high Platelet value
            if labcheck.abnormal_labcheck.platelet.abnormal_checker().get("highorlow") == "L":
                # Check if first LabCheck Lab was normal or high
                ### NEED TO CHECK HOW FAR BACK FIRST LABCHECK WAS, SIMILAR TO CREATININE WHICH ISN'T WORKING
                if (
                    labchecks[len(labchecks) - 1].platelet.abnormal_checker() == None
                    or labchecks[len(labchecks) - 1].platelet.abnormal_checker().get("highorlow") == "H"
                ):
                    # If Platelet value is < 75% the lower limit of normal (will be second in a row), raise urgent flag
                    # Will discontinue ULT and PPx, pause ULTPlan
                    if labcheck.platelet.var_x_low(0.75):
                        return "urgent"
                    else:
                        return None
                # If first LabCheck was low, evaluate how much it has dropped from the first value
                ### NEED TO CHANGE FIRST VALUE TO A BASELINE CALCULATOR METHOD
                else:
                    if labcheck.platelet.value <= (0.5 * labchecks[len(labchecks) - 1].platelet.value):
                        return "urgent"
                    elif labcheck.platelet.value <= (0.75 * labchecks[len(labchecks) - 1].platelet.value):
                        return "nonurgent"
                    else:
                        return None
            else:
                return "urgent"
        else:
            # LabCheck is not follow up for another abnormal_labcheck
            # If Platelet value is 50% the lower limit of normal, flag urgent, stopping ULT/PPx, pausing ULTPlan
            if labcheck.platelet.var_x_low(0.5):
                return "urgent"
            # If Platelet value is lower than the lower limit of normal, check if it's always low and if not, raise nonurgent follow up
            else:
                # Check if this is the first LabCheck, if so, continue normally
                if len(labchecks) == 1:
                    return None
                # Check if there are multiple LabChecks and, if so, if the baseline (initial) value is low
                if len(labchecks) > 1:
                    if labchecks[len(labchecks) - 1].platelet.abnormal_checker():
                        if labchecks[len(labchecks) - 1].platelet.abnormal_checker().get("highorlow") == "L":
                            return None
                        else:
                            return "nonurgent"
                    else:
                        return "nonurgent"
                else:
                    return "nonurgent"


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

    # Overwriting save() method to check if baseline is set to True, marks all others as False if so
    # Makes baseline unique for the model class for the User
    def save(self, *args, **kwargs):
        if not self.baseline:
            return super(WBC, self).save(*args, **kwargs)
        with transaction.atomic():
            WBC.objects.filter(user=self.user, baseline=True).update(baseline=False)
            return super(WBC, self).save(*args, **kwargs)

    def get_baseline(self):
        """Method that fetches the User's baseline WBC value.
        Returns baseline WBC value if so.
        Else returns None.
        """
        try:
            self.baseline = Platelet.objects.filter(user=self.user).get(baseline=True).values("value")
        except:
            self.baseline = None
        return self.baseline

    def abnormal_high(self, labcheck, labchecks):
        """Function that processes a high WBC.
        Takes a LabCheck and list of LabChecks as argument, the latter to avoid hitting the database multiple times with several different labs.

        Args:
            labcheck ([LabCheck]): [LabCheck the WBC is related to.]
            labchecks ([List]): [List of LabChecks provided by the function processing the abnormal WBC.]

        Returns:
            string or nothing: returns "urgent" if urgent LabCheck follow up required, nonurgent if non-urgent required
        """
        try:
            self.baseline = self.get_baseline()
        except:
            self.baseline = None

        # Check if there is a baseline WBC and if it is higher than the upper limit of normal
        # Process high WBC differently for patient with chronic leukocytosis (high WBC)
        if self.baseline:
            if self.baseline >= self.reference_upper:
                if labcheck.WBC.var_x_high(3, baseline=self.baseline):
                    return "urgent"
                elif labcheck.WBC.var_x_high(2, baseline=self.baseline):
                    return "nonurgent"
                else:
                    return None
        elif labcheck.abnormal_labcheck:
            pass
        else:
            # LabCheck is not follow up for another abnormal_labcheck
            # If Platelet value is 50% the lower limit of normal, flag urgent, stopping ULT/PPx, pausing ULTPlan
            # Check if this is the first LabCheck, if so, continue normally
            if len(labchecks) == 1:
                return None
            else:
                if labcheck.WBC.var_x_high(3):
                    return "urgent"
                elif labcheck.WBC.var_x_high(2):
                    return "nonurgent"
                else:
                    return None


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
    # Overwriting save() method to check if baseline is set to True, marks all others as False if so
    # Makes baseline unique for the model class for the User
    def save(self, *args, **kwargs):
        if not self.baseline:
            return super(Hemoglobin, self).save(*args, **kwargs)
        with transaction.atomic():
            Hemoglobin.objects.filter(user=self.user, baseline=True).update(baseline=False)
            return super(Hemoglobin, self).save(*args, **kwargs)


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
    # Overwriting save() method to check if baseline is set to True, marks all others as False if so
    # Makes baseline unique for the model class for the User
    def save(self, *args, **kwargs):
        if not self.baseline:
            return super(Creatinine, self).save(*args, **kwargs)
        with transaction.atomic():
            Creatinine.objects.filter(user=self.user, baseline=True).update(baseline=False)
            return super(Creatinine, self).save(*args, **kwargs)

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
                return None
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
                        return None
                else:
                    return None
        return None

    def stage_calculator(self):
        """Method that takes calculated eGFR and returns CKD stage

        Returns:
            [integer or None]: [integer corresponding to the CKD stage otherwise None]
        """
        eGFR = self.eGFR_calculator()
        if eGFR >= 90:
            return 1
        if 90 > eGFR >= 60:
            return 2
        if 60 > eGFR >= 30:
            return 3
        if 30 > eGFR >= 15:
            return 4
        if eGFR < 15:
            return 5
        else:
            return None

    def var_x_high(self, var):
        """
        Function that checks whether a lab value which is greater than the upper limit of normal is greater than input var times the upper limit of normal.
        Has to be overwritten for Creatinine to avoid multiplying float x decimal.
        Returns:
            bool: returns true if Lab.value is greater than var times the upper limit of normal
        """
        if self.value > (Decimal(var) * self.reference_upper):
            return True
        else:
            return False

    def find_baseline(self, labchecks=None):
        """Function that takes a Creatinine and finds the baseline Creatinine value for that Creatinine's User.
        Checks if User exists and has a ULTPlan and if Creatinine instance ULTPlan is also that User's ULTPlan.
        Takes optional labchecks argument to avoid hitting the database if it has already been done (for instance as part of a ULTPLan method)
        returns:
            Decimal: returns a Decimal Creatinine value
            else returns None
        """
        # Check if Creatinine has a User with a ULTPlan and that the Creatinine has a ULTPlan and it is the User's
        if self.user and self.user.ultplan and self.ultplan:
            if self.user.ultplan == self.ultplan:
                # Check if labchecks optional argument supplied, set to self.labchecks if so
                if labchecks:
                    self.labchecks = labchecks
                # If not, query for LabChecks associated with ULTPlan
                else:
                    self.labchecks = self.ultplan.labcheck_set.filter(completed=True).order_by("-completed_date")
                # If there is only 1 LabCheck and thus 1 Creatinine, set that to baseline
                if len(self.labchecks) == 1:
                    return self.labchecks[0].creatinine.value
                # If there is more than 1 LabCheck, check if the initial LabCheck Creatinine was normal
                # If so, set that to the baseline
                ### NEED TO INCLUDE SOME LOGIC TO SEE HOW FAR BACK IN TIME THIS WAS
                elif self.labchecks[len(labchecks) - 1].creatinine.abnormal_checker() == None:
                    # Check if initial LabCheck was over a year prior
                    if self.labchecks[len(labchecks) - 1].completed_date <= datetime.today().date() - timedelta(
                        days=365
                    ):
                        # If so, assemble a list of last year's Creatinines
                        last_year_creatinines = []
                        for labcheck in self.labchecks:
                            if self.labcheck.completed_date <= (datetime.today().date() - timedelta(days=365)):
                                last_year_creatinines.append(labcheck.creatinine.value)
                        # If there is more than 1 Creatinine drawn in the last year, return the minimum value that year to set baseline
                        if len(last_year_creatinines) > 1:
                            return min(last_year_creatinines)
                        # Otherwise return the initial normal value
                        else:
                            return self.labchecks[len(labchecks) - 1].creatinine.value
                    else:
                        return self.labchecks[len(labchecks) - 1].creatinine.value
                # If first LabCheck was abnormal, pick the lowest Creatinine value from all the observations and set that to baseline
                ### AGAIN NEED TO INCLUDE LOGIC TO SEE HOW FAR BACK IN TIME THIS GOES
                elif self.labchecks[len(labchecks) - 1].creatinine.abnormal_checker():
                    # Check if initial LabCheck was over a year prior
                    if self.labchecks[len(labchecks) - 1].completed_date <= (
                        datetime.today().date() - timedelta(days=365)
                    ):
                        # If so, assemble a list of last year's Creatinines
                        last_year_creatinines = []
                        for labcheck in self.labchecks:
                            if self.labcheck.completed_date <= (datetime.today().date() - timedelta(days=365)):
                                last_year_creatinines.append(labcheck.creatinine.value)
                        # If there is at least 1 Creatinine drawn in the last year, return the minimum value that year to set baseline
                        if last_year_creatinines:
                            return min(last_year_creatinines)
                        # Otherwise, return initial value
                        ### NEED TO DIAL BACK ANOTHER YEAR, PERHAPS RECURSIVELY, TO RETURN VALUE
                        else:
                            return self.labchecks[len(labchecks) - 1].creatinine.value
            else:
                return None
        else:
            return None

    def var_x_baseline_high(self, var, baseline):
        """Function that takes a percentage and calculates whether a Lab value is that percentage of a baseline Lab value specified by the function.
        Has to be overwritten for Creatinine to avoid multiplying float x decimal.

        Args:
            var (Float): Float percentage for calculating where the current Lab value is relative to baseline
            baseline (Lab.value): Lab value argument for comparing the current Lab value to.
        Returns:
            bool: True if Lab.value is var * baseline, False if not
        """
        if self.value > (Decimal(var) * baseline):
            return True
        else:
            return False

    def abnormal_high(self, labcheck, labchecks):
        """Function that processes a high creatinine.
        Takes a LabCheck and list of LabChecks as argument, the latter to avoid hitting the database multiple times with several different labs.

        Args:
            labcheck ([LabCheck]): [LabCheck the Creatinine is related to.]
            labchecks ([List]): [List of LabChecks provided by the function processing the abnormal Creatinine.]

        Returns:
            string or nothing: returns "urgent" if urgent LabCheck follow up required, nonurgent if non-urgent required
        """
        # Check if labcheck is a follow up on an abnormal_labcheck
        # If so, process differently
        if labcheck.abnormal_labcheck:
            # Check if first LabCheck creatinine was abnormal
            if labchecks[len(labchecks) - 1].creatinine.abnormal_checker() == None:
                # If LabCheck Creatinine is > 2 times the upper limit of normal, schedule urgent LabCheck
                # Discontinue ULT and PPx, pause ULTPlan
                if labcheck.creatinine.var_x_baseline_high(2, self.find_baseline(labchecks=labchecks)):
                    return "urgent"
                # If LabCheck Creatinine is < 1.5 times the upper limit of normal, schedule urgent LabCheck.
                # Continue ULT, PPx, ULTPlan
                elif labcheck.creatinine.var_x_baseline_high(1.5, self.find_baseline(labchecks=labchecks)):
                    return "nonurgent"
            # If first LabCheck Creatinine was abnormal, fluctuations will be larger so have more stringent criteria for follow up labs and ULTPlan modification
            elif labchecks[len(labchecks) - 1].creatinine.abnormal_checker():
                # If LabCheck Creatinine is > 1.5 times the upper limit of normal, schedule urgent LabCheck.
                # Discontinue ULT and PPx, pause ULTPlan
                if labcheck.creatinine.var_x_baseline_high(1.5, self.find_baseline(labchecks=labchecks)):
                    return "urgent"
                # If LabCheck Creatinine is < 1.25 times the upper limit of normal, schedule urgent LabCheck
                # But continue medications, don't pause ULTPlan
                elif labcheck.creatinine.var_x_baseline_high(1.25, self.find_baseline(labchecks=labchecks)):
                    return "nonurgent"
        else:
            # Check if there is only one completed LabCheck
            # If so, check if User MedicalProfile has CKD == True, if not, calculate stage and mark == True
            if len(labchecks) == 1:
                # If this is the User's first LabCheck, mark CKD on MedicalProfile to True because creatinine is abnormal.
                if self.user.medicalprofile.CKD.value == False:
                    self.user.medicalprofile.CKD.value == True
                    # Calculate CKD stage if eGFR can be calculated
                    if self.user.medicalprofile.CKD.eGFR_calculator():
                        self.user.medicalprofile.CKD.stage = self.user.medicalprofile.CKD.stage_calculator()
                    self.user.medicalprofile.CKD.save()
            # Check if first LabCheck creatinine was abnormal
            elif labchecks[len(labchecks) - 1].creatinine.abnormal_checker() == None:
                # If LabCheck Creatinine is > 2 times the upper limit of normal, schedule urgent LabCheck
                # Discontinue ULT and PPx, pause ULTPlan
                if labcheck.creatinine.var_x_baseline_high(2, self.find_baseline(labchecks=labchecks)):
                    return "urgent"
                # If LabCheck Creatinine is < 1.5 times the upper limit of normal, schedule urgent LabCheck.
                # Continue ULT, PPx, ULTPlan
                elif labcheck.creatinine.var_x_baseline_high(1.5, self.find_baseline(labchecks=labchecks)):
                    return "nonurgent"
            # If first LabCheck Creatinine was abnormal, fluctuations will be larger so have more stringent criteria for follow up labs and ULTPlan modification
            elif labchecks[len(labchecks) - 1].creatinine.abnormal_checker():
                # If LabCheck Creatinine is > 1.5 times the upper limit of normal, schedule urgent LabCheck.
                # Discontinue ULT and PPx, pause ULTPlan
                if labcheck.creatinine.var_x_baseline_high(1.5, self.find_baseline(labchecks=labchecks)):
                    return "urgent"
                # If LabCheck Creatinine is < 1.25 times the upper limit of normal, schedule urgent LabCheck
                # But continue medications, don't pause ULTPlan
                elif labcheck.creatinine.var_x_baseline_high(1.25, self.find_baseline(labchecks=labchecks)):
                    return "nonurgent"


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
        # Check if LabCheck completed
        if self.completed == True:
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
        # Return None if LabCheck not completed
        else:
            return None

    def __str__(self):
        if self.completed == True:
            return f"{str(self.user).capitalize()}'s lab check completed {self.completed_date}"
        else:
            return f"{str(self.user).capitalize()}'s lab check due {self.due}"

    def get_absolute_url(self):
        return reverse("ultplan:detail", kwargs={"pk": self.ultplan.pk})
