from datetime import datetime, timedelta
from decimal import *
from statistics import mean

from django.conf import settings
from django.db import models, transaction
from django.urls import reverse
from django.utils.text import slugify
from django_extensions.db.models import TimeStampedModel
from simple_history.models import HistoricalRecords

from ..lab.choices import BOOL_CHOICES, CELLSMM3, GDL, MGDL, PLTMICROL, UL, UNIT_CHOICES


class Lab(TimeStampedModel):
    def class_name(self):
        return self.__class__.__name__

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date_drawn = models.DateField(help_text="What day was this lab drawn?", default=None, null=True, blank=True)
    abnormal_followup = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, default=None)
    history = HistoricalRecords(inherit=True)
    slug = models.SlugField(max_length=200, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name} {self.value} {self.units}"

    def get_absolute_url(self):
        return reverse("lab:detail", kwargs={"lab": self.name, "slug": self.slug})

    def __unicode__(self):
        return self.name

    @property
    def low(self):
        """
        Function that checks whether a Lab.value is less than the lower limit of normal.

        Returns:
            bool: returns True if Lab.value is less than the lower limit of normal, False if not.
        """
        if self.value < self.reference_lower:
            return True
        else:
            return False

    @property
    def high(self):
        """
        Function that checks whether a Lab.value is greater than the upper limit of normal.

        Returns:
            bool: returns True if Lab.value is greater than the upper limit of normal, False if not.
        """
        if self.value > self.reference_upper:
            return True
        else:
            return False

    @property
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

    @property
    def abnormal(self):
        """
        Function that checks whether or not a Lab.value is abnormal.
        If lab is abnormal, set abnormal_flag attribute to True.

        Returns:
            dictionary or None: Returns a dictionary with descriptors of the Lab.value abnormality if present, otherwise returns None
        """
        # Check if lab is lower than reference range
        if self.low:
            return "L"
        elif self.high:
            if self.three_x_high:
                return "!H!"
            else:
                return "H"


class Urate(Lab):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name=("urate_creator"),
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

    # Creates slug if not present
    def save(self, *args, **kwargs):
        super(Urate, self).save(*args, **kwargs)
        # Check if there isn't a slug
        if not self.slug:
            # If there isn't, check if there's a user
            if self.user:
                # If so, create slug from user and pk
                self.slug = slugify(self.user.username) + "-" + str(self.id)


class ALT(Lab):
    LOWER_LIMIT = 7
    UPPER_LIMIT = 55

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name=("alt_creator"),
    )
    value = models.IntegerField(help_text="ALT (SGPT) is typically reported in units per liter (U/L)")
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True, default=UL)
    name = "ALT"
    reference_lower = models.IntegerField(default=LOWER_LIMIT, help_text="Lower limit of normal values for ALT")
    reference_upper = models.IntegerField(default=UPPER_LIMIT, help_text="Upper limit of normal values for ALT")

    # Creates slug if not present
    def save(self, *args, **kwargs):
        super(ALT, self).save(*args, **kwargs)
        # Check if there isn't a slug
        if not self.slug:
            # If there isn't, check if there's a user
            if self.user:
                # If so, create slug from user and pk
                self.slug = slugify(self.user.username) + "-" + str(self.id)


class BaselineALT(ALT):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    value = models.IntegerField(
        help_text="ALT (SGPT) is typically reported in units per liter (U/L)", null=True, blank=True
    )
    name = "baseline_ALT"
    date_drawn = None
    abnormal_followup = None

    # Creates slug if not present
    def save(self, *args, **kwargs):
        super(BaselineALT, self).save(*args, **kwargs)
        # Check if there isn't a slug
        if not self.slug:
            # If there isn't, check if there's a user
            if self.user:
                # If so, create slug from user and pk
                self.slug = slugify(self.user.username)


class AST(Lab):
    LOWER_LIMIT = 10
    UPPER_LIMIT = 40

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name=("ast_creator"),
    )
    value = models.IntegerField(help_text="AST (SGOT) is typically reported in units per liter (U/L)")
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True, default=UL)
    name = "AST"
    reference_lower = models.IntegerField(default=LOWER_LIMIT, help_text="Lower limit of normal values for AST")
    reference_upper = models.IntegerField(default=UPPER_LIMIT, help_text="Upper limit of normal values for AST")

    # Creates slug if not present
    def save(self, *args, **kwargs):
        super(AST, self).save(*args, **kwargs)
        # Check if there isn't a slug
        if not self.slug:
            # If there isn't, check if there's a user
            if self.user:
                # If so, create slug from user and pk
                self.slug = slugify(self.user.username) + "-" + str(self.id)


class BaselineAST(AST):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    value = models.IntegerField(
        help_text="AST (SGOT) is typically reported in units per liter (U/L)", null=True, blank=True
    )
    name = "baseline_AST"
    date_drawn = None
    abnormal_followup = None

    # Creates slug if not present
    def save(self, *args, **kwargs):
        super(BaselineAST, self).save(*args, **kwargs)
        # Check if there isn't a slug
        if not self.slug:
            # If there isn't, check if there's a user
            if self.user:
                # If so, create slug from user and pk
                self.slug = slugify(self.user.username)


class Platelet(Lab):
    LOWER_LIMIT = 150
    UPPER_LIMIT = 450

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name=("platelet_creator"),
    )
    value = models.IntegerField(
        help_text="PLT (platelets) is typically reported in platelets per microliter (PLT/microL)"
    )
    units = models.CharField(max_length=100, choices=UNIT_CHOICES, null=True, blank=True, default=PLTMICROL)
    name = "platelet"
    reference_lower = models.IntegerField(default=LOWER_LIMIT, help_text="Lower limit of normal values for platelets")
    reference_upper = models.IntegerField(default=UPPER_LIMIT, help_text="Upper limit of normal values for platelets")

    # Creates slug if not present
    def save(self, *args, **kwargs):
        super(Platelet, self).save(*args, **kwargs)
        # Check if there isn't a slug
        if not self.slug:
            # If there isn't, check if there's a user
            if self.user:
                # If so, create slug from user and pk
                self.slug = slugify(self.user.username) + "-" + str(self.id)

    def get_baseline(self):
        """Method that fetches the User's baseline Platelet value.
        Returns baseline Platelet value if so.
        Else returns None.
        """
        if self.user.thrombocytopenia.baseline:
            return self.user.thrombocytopenia.baseline
        if self.user.thrombcytosis.baseline:
            return self.user.thrombocytosis.baseline
        try:
            self.baseline = Platelet.objects.filter(user=self.user).get(baseline=True).value
        except:
            self.baseline = None
        return self.baseline

    def process_high(self, labcheck, labchecks):
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


class BaselinePlatelet(Platelet):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    value = models.IntegerField(
        help_text="PLT (platelets) is typically reported in platelets per microliter (PLT/microL)",
        null=True,
        blank=True,
    )
    name = "baseline_platelet"
    date_drawn = None
    abnormal_followup = None

    # Creates slug if not present
    def save(self, *args, **kwargs):
        super(BaselinePlatelet, self).save(*args, **kwargs)
        # Check if there isn't a slug
        if not self.slug:
            # If there isn't, check if there's a user
            if self.user:
                # If so, create slug from user and pk
                self.slug = slugify(self.user.username)


class WBC(Lab):
    LOWER_LIMIT = Decimal(4.5)
    UPPER_LIMIT = Decimal(11.0)

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name=("wbc_creator"),
    )
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

    # Creates slug if not present
    def save(self, *args, **kwargs):
        super(WBC, self).save(*args, **kwargs)
        # Check if there isn't a slug
        if not self.slug:
            # If there isn't, check if there's a user
            if self.user:
                # If so, create slug from user and pk
                self.slug = slugify(self.user.username)

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

    def process_high(self, labcheck, labchecks):
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


class BaselineWBC(WBC):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    value = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        help_text="WBC (white blood cells) is typically reported as cells per cubic millimeter (cells/mm^3)",
        null=True,
        blank=True,
    )
    name = "baseline_WBC"
    date_drawn = None
    abnormal_followup = None

    # Creates slug if not present
    def save(self, *args, **kwargs):
        super(BaselineWBC, self).save(*args, **kwargs)
        # Check if there isn't a slug
        if not self.slug:
            # If there isn't, check if there's a user
            if self.user:
                # If so, create slug from user and pk
                self.slug = slugify(self.user.username)


class Hemoglobin(Lab):
    LOWER_LIMIT = Decimal(13.5)
    UPPER_LIMIT = Decimal(17.5)

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name=("hemoglobin_creator"),
    )
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
    # Creates slug if not present
    def save(self, *args, **kwargs):
        super(Hemoglobin, self).save(*args, **kwargs)
        # Check if there isn't a slug
        if not self.slug:
            # If there isn't, check if there's a user
            if self.user:
                # If so, create slug from user and pk
                self.slug = slugify(self.user.username)


def round_decimal(value, places):
    if value is not None:
        # see https://docs.python.org/2/library/decimal.html#decimal.Decimal.quantize for options
        return value.quantize(Decimal(10) ** -places)
    return value


class BaselineHemoglobin(Hemoglobin):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    value = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        help_text="HGB (hemoglobin) is typically reporeted in grams per deciliter (g/dL)",
        null=True,
        blank=True,
    )
    name = "baseline_hemoglobin"
    date_drawn = None
    abnormal_followup = None
    # Creates slug if not present
    def save(self, *args, **kwargs):
        super(BaselineHemoglobin, self).save(*args, **kwargs)
        # Check if there isn't a slug
        if not self.slug:
            # If there isn't, check if there's a user
            if self.user:
                # If so, create slug from user and pk
                self.slug = slugify(self.user.username)


class Creatinine(Lab):
    LOWER_LIMIT = Decimal(0.74)
    UPPER_LIMIT = Decimal(1.35)

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name=("creatinine_creator"),
    )
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
    # Also creates slug if not present yet
    def save(self, *args, **kwargs):
        if not self.id:
            if not self.date_drawn:
                self.date_drawn = datetime.today().date()
        super(Creatinine, self).save(*args, **kwargs)
        # Check if there is a user field
        if self.user:
            # If there is, check if a slug field has been set
            if not self.slug:
                # If no slug but has a user, it is a newly created object and needs slug set
                self.slug = slugify(self.user.username) + "-" + str(self.id)
        if not self.baseline:
            return super(Creatinine, self).save()
        with transaction.atomic():
            Creatinine.objects.filter(user=self.user, baseline=True).update(baseline=False)
            return super(Creatinine, self).save()

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
        else:
            return Decimal(1.00)

    def sex_modifier(self):
        if self.user.patientprofile.gender == "male":
            return Decimal(1.018)
        elif self.user.patientprofile.gender == "female":
            return Decimal(1.00)
        else:
            return False

    def eGFR_calculator(self):
        if self.user.patientprofile.age == None:
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
                        * Decimal(0.993) ** self.user.patientprofile.age
                        * self.race_modifier()
                        * self.sex_modifier()
                    )
                    return round_decimal(eGFR, 2)

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

    @classmethod
    def set_baseline(cls, user):
        """
        Class method that sets a User's BaselineCreatinine
        Also modifies User's CKD to reflect BaselineCreatinine

        Args: user = User object

        Returns:
            Nothing or None, modifies related data
        """
        # Assemble list of Creatinines for User
        creatinines = Creatinine.objects.filter(user=user)
        # If no creatinines, return None
        if len(creatinines) == 0:
            return None
        # If 1 creatinine, that must be the baseline
        if len(creatinines) == 1:
            user.baselinecreatinine.value = creatinines[0].value
            user.baselinecreatinine.save()
        else:
            # Else assemble list of creatinines from t-365 > t-7 days
            # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3338282/
            creatinines = creatinines.filter(
                date_drawn__range=[
                    (datetime.today().date() - timedelta(days=365)),
                    datetime.today().date() - timedelta(days=7),
                ]
            )
            # If there are no creatinines over last year, look back 2 years
            if len(creatinines) == 0:
                creatinines = creatinines.filter(
                    date_drawn__range=[
                        (datetime.today().date() - timedelta(days=730)),
                        datetime.today().date() - timedelta(days=7),
                    ]
                )
            # If no creatinines over last 2 years, return None
            if len(creatinines) == 0:
                return None
            # Find mean over last year(s)
            mean_creatinine = mean(creatinine.value for creatinine in creatinines)
            user.baselinecreatinine.value = mean_creatinine.value
            user.baselinecreatinine.save()
            if user.ckd.value != True:
                user.ckd.value = True
                if user.baselinecreatinine.eGFR_calculator():
                    if user.baselinecreatinine.stage_calculator():
                        user.ckd.stage = user.baselinecreatinine.stage_calculator()
            user.ckd.save()

    @classmethod
    def diagnose_ckd(cls, user):
        """
        Class method that will determine if a user has CKD
        Checks for persistently abnormal renal function (eGFR) for 90 days or longer
        Any eGFR > 60 will result in a False return

        Args: user
        ***REQUIRES USER TO HAVE RACE, SEX, and AGE TO CALCULATE eGFR***
        Returns: Boolean, but modifies user.ckd first
        If True: will set user.ckd to True, assign user.ckd.baseline, set user.ckd.stage
                 will also set user.ckd.baseline.baseline to True
        If False: will set user.ckd to False, remove user.ckd.baseline/stage
                  will also set.user.ckd.baseline.baseline to False
        """
        # https://www.kidney-international.org/article/S0085-2538(15)50698-4/fulltext
        # Check if user has CKD already
        if user.ckd.value == True:
            return True
        # Assemble chronolocical list of creatinines, blank list of eGFRs
        creatinines = Creatinine.objects.filter(user=user).order_by("-date_drawn")
        # Declare list of eGFRs for scope
        eGFRs = []
        # Assemble eGFR/Creatinine list via eGFR_calculator() on each creatinine
        for creatinine in creatinines:
            eGFR = creatinine.eGFR_calculator()
            eGFRs.append([eGFR, creatinine])
        # Iterate over eGFR/Creatinine list
        for eGFR_index in range(len(eGFRs)):
            eGFR = eGFRs[eGFR_index][0]
            creatinine = eGFRs[0][1]
            # If any eGFR is > 60, there is no CKD, process User data accordingly
            if eGFR > 60:
                if user.ckd.value == True:
                    user.ckd.value = False
                    user.ckd.stage = None
                    user.ckd.save()
                if user.baselinecreatinine:
                    user.baselinecreatinine.value = None
                    user.baselinecreatinine.save()
                return False
            # If eGFR is < 60
            else:
                # Check if list index is not the last item in the list
                # Check if subsequent eGFR is abnormal
                if eGFR_index < (len(eGFRs) - 1):
                    next_eGFR = eGFRs[eGFR_index + 1][0]
                    next_creatinine = eGFRs[eGFR_index + 1][1]
                    # If not, User does not have CKD, process Profile accordingly
                    if next_eGFR > 60:
                        if user.ckd.value == True:
                            user.ckd.value = False
                            user.ckd.stage = None
                            user.ckd.save()
                        if user.baselinecreatinine:
                            user.baselinecreatinine.value = None
                            user.baselinecreatinine.save()
                        return False
                    # If eGFR is again < 60
                    # Check if the current index's creatine.date_drawn is 90 days or more from the initial
                    else:
                        if creatinine.date_drawn - next_creatinine.date_drawn > timedelta(days=90):
                            # If all creatinines abnormal and 90 days or more apart, set_baseline
                            user.baselinecreatinine.set_baseline(user=user)
                            return True
                else:
                    return False

    def var_x_high(self, var):
        """
        Method that calculates if a lab value is higher by a %=var.
        Takes optional baseline argument.
        Otherwise uses reference_upper for calculation.
        Has to be overwritten for Creatinine to avoid multiplying float x decimal.

        Args:
            var (Float): Float percentage for calculating where the current Lab value is relative to baseline
            baseline (Lab.value): Lab value argument for comparing the current Lab value to.
        Returns:
            bool: True if Lab.value is var * baseline, False if not
        """
        baseline = self.get_baseline()

        if baseline:
            if self.value > (Decimal(var) * baseline):
                return True
            else:
                return False
        else:
            if self.value > (Decimal(var) * self.reference_upper):
                return True
            else:
                return False

    def process_high(self):
        """
        Function that processes a high creatinine.
        First sees if the User has CKD and a baseline Creatinine.
        Then checks if this object is a follow up an abnormal Creatinine.
        Returns "urgent" for emergent rise in Cr (ARF).
        Will stop ULTPlan.
        Returns "nonurgent" for close follow-up
        If high Creatinine is an abnormal follow up but not "urgent":
            Recalculates baseline in CKD, checks for CKD otherwise
        Returns:
            string or nothing: returns "urgent" if urgent LabCheck follow up required, nonurgent if non-urgent required
        """
        # Declare baseline for scope
        self.baseline = None
        # See if the User meets the definition of CKD
        if self.self.diagnose_ckd() == True:
            # Try to fetch baseline
            self.baseline = self.get_baseline()
        # Check if Creatinine is a follow up on an abnormal
        if self.abnormal_followup:
            # Check if User has baseline Creatinine (=CKD)
            if self.baseline:
                if self.var_x_high(1.5, baseline=self.baseline):
                    return "urgent"
                elif self.var_x_high(1.25, baseline=self.baseline):
                    self.set_baseline(user=self.user)
                    return "nonurgent"
                else:
                    self.set_baseline(user=self.user)
            # If no baseline Creatinine
            else:
                if self.var_x_high(1.5):
                    return "urgent"
                elif self.var_x_high(1.25):
                    self.diagnose_ckd(user=self.user)
                    return "nonurgent"
                else:
                    self.diagnose_ckd(user=self.user)
        # If Creatinine isn't a follow up on an abnormal
        else:
            # Check if User has baseline Creatinine
            if self.baseline:
                if self.var_x_high(1.5, baseline=self.baseline):
                    return "urgent"
                elif self.var_x_high(1.25, baseline=self.baseline):
                    return "nonurgent"
            # If no baseline Creatinine
            else:
                if self.var_x_high(1.5):
                    return "urgent"
                elif self.var_x_high(1.25):
                    return "nonurgent"


class BaselineCreatinine(Creatinine):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    value = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        help_text="Creatinine is typically reported as milligrams per deciliter (mg/dL)",
        null=True,
        blank=True,
    )
    name = "baseline_creatinine"
    date_drawn = None
    abnormal_followup = None
    # Creates slug if not present
    def save(self, *args, **kwargs):
        super(BaselineCreatinine, self).save(*args, **kwargs)
        # Check if there isn't a slug
        if not self.slug:
            # If there isn't, check if there's a user
            if self.user:
                # If so, create slug from user and pk
                self.slug = slugify(self.user.username)


class LabCheck(TimeStampedModel):
    """Model to coordinate labs for monitoring ULTPlan titration."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name=("labcheck_creator"),
    )
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
    history = HistoricalRecords()
    slug = models.SlugField(max_length=200, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            # Check if there is a user field
            if self.user:
                # If there's a user, add slug field
                self.slug = (
                    slugify(self.user.username) + "-" + str((LabCheck.objects.filter(user=self.user).count() + 1))
                )
        super(LabCheck, self).save(*args, **kwargs)

    @property
    def delinquent(self):
        if datetime.today().date() >= self.due - self.ultplan.delinquent_lab_interval:
            return True
        else:
            return True

    @property
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
        return reverse("ultplan:detail", kwargs={"slug": self.ultplan.slug})
