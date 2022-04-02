from datetime import datetime, timedelta
from decimal import Decimal
from math import ceil
from statistics import mean

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.fields import BooleanField
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django_extensions.db.models import TimeStampedModel
from simple_history.models import HistoricalRecords

from ..lab.choices import BOOL_CHOICES, CELLSMM3, GDL, MGDL, PLTMICROL, UL, UNIT_CHOICES


def round_decimal(value, places):
    if value is not None:
        # see https://docs.python.org/2/library/decimal.html#decimal.Decimal.quantize for options
        return value.quantize(Decimal(10) ** -places)
    return value


class Lab(TimeStampedModel):
    def class_name(self):
        return self.__class__.__name__

    class Flag(models.IntegerChoices):
        """
        class to describe Lab.flag field choices and interpretation the Lab.value.
        Will be set by process_high() or process_low() method.
        """

        # Lab is normal, continue as normal, default value
        NORMAL = 0
        # Lab.value is high or low, but not of clinical consequence
        # Continue ULTPlan as usual
        TRIVIAL = 1
        # Lab.value is non-urgently abnormal.
        # Will not pause ULTPlan
        NONURGENT = 2
        # Lab.value is urgently abnormal.
        # WILL PAUSE ULTPLAN
        URGENT = 3
        # Lab.value is emergently abnormal.
        # WILL PAUSE ULPLAN
        # WILL RECOMMEND SEEKING IN PERSON MEDICAL CONSULTATION
        EMERGENCY = 4
        # Lab.value is close to normal.
        # Set when a Lab is a follow-up (has abnormal_followup field)
        RESOLVED = 5
        # Lab.value is stable from the last abnormal check
        STABLE = 6
        # Lab.value is improving from the last abnormal check.
        IMPROVING = 7

    class Action(models.IntegerChoices):
        """
        Class to describe Lab.action field choices and action taken on abnormal Lab.
        Will be set by process_high() or process_low() method.
        """

        # Continue the ULTPlan as normal
        CONTINUE = 0
        # Recheck the Lab non-urgently
        # Meant for a non-urgent lab abnormality
        RECHECK = 1
        # Pause the ULTPlan and recheck the Lab urgently
        # Meant for a serious but non-emergent lab abnormality
        PAUSE = 2
        # Change the ULTPlan
        # Will also prompt inactivation of current ULTPlan in order to create a new active one
        ### TO DO: BUILD ULTPLAN change() METHOD ###
        CHANGE = 3
        # Pause the ULTPLan for an emergency, meant to be resumed or the ULTPlan stopped
        ### TO DO: BUILD ULTPLAN RESUME() and INACTIVATE() METHODS ###
        EMERGENCY = 4
        # Permanently discontinue ULTPlan
        INACTIVATE = 5

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date_drawn = models.DateTimeField(help_text="What day was this lab drawn?", default=None, null=True, blank=True)
    abnormal_followup = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, default=None)
    history = HistoricalRecords(inherit=True)
    slug = models.SlugField(max_length=200, null=True, blank=True)
    flag = models.IntegerField(
        choices=Flag.choices, default=0, validators=[MinValueValidator(0), MaxValueValidator(7)], null=True, blank=True
    )
    action = models.IntegerField(
        choices=Action.choices,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        null=True,
        blank=True,
    )

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

    @property
    def show_flag(self):
        """
        Function that displays the Lab's flag attribute.
        Returns: string
        """
        if self.flag == 0:
            return "normal"
        elif self.flag == 1:
            return "trivial"
        elif self.flag == 2:
            return "nonurgent"
        elif self.flag == 3:
            return "urgent"
        elif self.flag == 4:
            return "emergency"
        elif self.flag == 5:
            return "resolved"
        elif self.flag == 6:
            return "stable"
        elif self.flag == 7:
            return "improving"
        else:
            return None

    @property
    def show_action(self):
        """
        Function that displays the Lab's flag attribute.
        Returns: string
        """
        if self.flag == 0:
            return "continue"
        elif self.flag == 1:
            return "recheck"
        elif self.flag == 2:
            return "pause"
        elif self.flag == 3:
            return "change"
        elif self.flag == 4:
            return "emergency"
        elif self.flag == 5:
            return "inactivate"
        else:
            return None

    def var_x_high(self, var):
        """
        Calculates if a Lab value is higher by a percentage (var).
        Tries to fetch BaselineLab for User for calculation.
        Otherwise uses reference_upper for calculation.

        Args:
            var (Float): Float percentage for calculating where the current Lab value is relative to baseline
        Returns:
            bool: True if Lab.value is > var * baseline, False if not
        """
        baseline = self.get_baseline()

        if baseline:
            if self.value > (var * baseline.value):
                return True
            else:
                return False
        else:
            if self.value > (var * self.reference_upper):
                return True
            else:
                return False

    def get_baseline(self):
        """
        Method that gets a User's Baseline for any Lab
        Returns: BaselineLab or none
        """
        return getattr(self.user, "baseline" + self.class_name().lower(), None)

    def get_labcheck(self):
        """
        Method that gets LabCheck associated with Lab
        returns: LabCheck object or None
        """
        # Check if Lab has LabCheck
        return getattr(self, "labcheck", None)

    def process_high(self):
        """
        Function that processes a high Lab.
        Checks if this object is a follow up an abnormal Lab.
        Returns "urgent" or "emergency" for emergent rise in Lab.
        Will stop ULTPlan. "emergency" will prompt a User seek immediate medical attention.
        Returns "nonurgent" for close follow-up, "trivial" for a small elevation that doesn't require immediate follow up.
        If high Lab is an abnormal follow up but not "urgent":
            Recalculates baseline in BaselineLab, checks for associated MedicalProfile object (CKD, transaminitis, leukopenia, etc.)
        Returns:
            string or nothing: returns "urgent" if urgent LabCheck follow up required, nonurgent if non-urgent required
        """
        # Assign percentages for processing high/low for scope
        trivial = None
        nonurgent = None
        urgent = None
        emergency = None

        # Check model to set percentages on which to process high values
        # Pulled from PatientProfile, which will automatically be created with default values
        if self.class_name() == "ALT" or self.class_name() == "AST":
            trivial = self.user.patientprofile.lft_trivial
            nonurgent = self.user.patientprofile.lft_nonurgent
            urgent = self.user.patientprofile.lft_urgent
            emergency = self.user.patientprofile.lft_emergency
        elif self.class_name() == "creatinine":
            trivial = self.user.patientprofile.creatinine_trivial
            nonurgent = self.user.patientprofile.creatinine_nonurgent
            urgent = self.user.patientprofile.creatinine_urgent
            emergency = self.user.patientprofile.creatinine_emergency
        elif self.class_name() == "WBC":
            trivial = self.user.patientprofile.wbc_high_trivial
            nonurgent = self.user.patientprofile.wbc_high_nonurgent
            urgent = self.user.patientprofile.wbc_high_urgent
            emergency = self.user.patientprofile.wbc_high_emergency
        elif self.class_name() == "platelet":
            trivial = self.user.patientprofile.platelet_high_trivial
            nonurgent = self.user.patientprofile.platelet_high_nonurgent
            urgent = self.user.patientprofile.platelet_high_urgent
            emergency = self.user.patientprofile.platelet_high_emergency
        elif self.class_name() == "hemoglobin":
            trivial = self.user.patientprofile.hemoglobin_high_trivial
            nonurgent = self.user.patientprofile.hemoglobin_high_nonurgent
            urgent = self.user.patientprofile.hemoglobin_high_urgent
            emergency = self.user.patientprofile.hemoglobin_high_emergency

        # Declare baseline for scope
        self.baseline = None
        # See if the User meets the definition of Transaminitis (=chronic hepatitis)
        if self.diagnose_transaminitis() == True:
            # Try to fetch baseline
            self.baseline = self.get_baseline()
        # Check if Lab is a follow up on an abnormal
        if self.abnormal_followup:
            # Emergency (flag=4) values will not flag a follow up lab
            # Will instead recommend user see medical attention
            # Otherwise:
            # If follow-up Lab at or below User's baseline, the original abnormality was likely an error
            if self.var_x_high(1) == False:
                self.abnormal_followup.flag = 5
                self.abnormal_followup.save()
                # Will return None at end of method
            # If follow-up is still 3x the upper limit of normal or User's baseline
            # Trigger emergency
            # This would mean 2 Labs sequentially that are > 100, potentially higher
            if self.var_x_high(urgent):
                self.flag = 4
                self.save()
                return "emergency"
            else:
                # If the abnormal original was "urgent"
                if self.abnormal_followup.flag == 3:
                    # Check if the follow up isn't 2x the baseline
                    # If not, save Lab.flag as improving and restart ULTPlan
                    if self.var_x_high(nonurgent) == False:
                        self.flag = 6
                        self.save()
                        return "improving_restart"
                    # Else the Lab is improving, but not enough to restart the ULTPlan yet
                    else:
                        self.flag = 7
                        self.save()
                        return "improving_recheck"
                # Else the abnormal original was "nonurgent" flag=2
                # If still 2x the baseline
                # Mark as urgent (Lab.flag=3)
                else:
                    if self.var_x_high(nonurgent):
                        self.flag = 3
                        self.save()
                        return "urgent"
                    else:
                        self.flag = 6
                        self.save()
                        return "improving_restart"
        # If Lab isn't a follow up on an abnormal
        else:
            if self.var_x_high(emergency):
                self.flag = 4
                self.save()
                return "emergency"
            elif self.var_x_high(urgent):
                self.flag = 3
                self.save()
                return "urgent"
            elif self.var_x_high(nonurgent):
                self.flag = 2
                self.save()
                return "nonurgent"
            elif self.var_x_high(trivial):
                self.flag = 1
                self.save()
        return None


class BaseALT(Lab):
    class Meta:
        abstract = True

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


class BaseAST(Lab):
    class Meta:
        abstract = True

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


class BaseCreatinine(Lab):
    class Meta:
        abstract = True

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

    def set_baseline(self):
        """
        Method that sets a User's BaselineCreatinine
        Also modifies User's CKD to reflect BaselineCreatinine
        ***WILL NOT MODIFY A USER-SET BASELINE (baseline.calculated == False)***

        Returns:
            Nothing or None, modifies related data
        """
        # Assemble list of Creatinines for User
        creatinines = Creatinine.objects.filter(user=self.user).order_by("-date_drawn")
        # If no creatinines, return None
        if len(creatinines) == 0:
            return None
        # If 1 creatinine, that must be the baseline
        if len(creatinines) == 1:
            baseline = self.get_baseline()
            # Check if there's a baseline
            if baseline:
                # If it's User-entered, don't change baseline
                if baseline.calculated == False:
                    return None
                # If not, set baseline to only Creatinine
                else:
                    baseline.value = creatinines[0].value
                    baseline.save()
                    self.user.ckd.last_modified = "Behind the scenes"
                    self.user.ckd.save()
            else:
                baseline = BaselineCreatinine.objects.create(
                    user=self.user, value=creatinines[0].value, calculated=True
                )
                if self.user.ckd.value == False:
                    self.user.ckd.value = True
                self.user.ckd.baseline = baseline
                self.user.ckd.last_modified = "Behind the scenes"
                self.user.ckd.save()
                baseline.value = creatinines[0].value
                baseline.save()
        else:
            # Else assemble list of creatinines from t-365 > t-7 days
            # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3338282/
            creatinines = creatinines.filter(
                date_drawn__range=[
                    (timezone.now() - timedelta(days=365)),
                    timezone.now() - timedelta(days=7),
                ]
            )
            # If there are no creatinines over last year, look back 2 years
            if len(creatinines) == 0:
                creatinines = Creatinine.objects.filter(
                    user=self.user,
                    date_drawn__range=[
                        (timezone.now() - timedelta(days=730)),
                        timezone.now() - timedelta(days=7),
                    ],
                ).order_by("-date_drawn")
            # If no creatinines over last 2 years, return None
            if len(creatinines) == 0:
                return None
            # Find mean over last year(s)
            mean_creatinine = Decimal(mean(creatinine.value for creatinine in creatinines))
            baseline = self.get_baseline()
            if baseline:
                if baseline.calculated == False:
                    return None
                else:
                    baseline.value = mean_creatinine
                    baseline.save()
            else:
                baseline = BaselineCreatinine.objects.create(user=self.user, value=mean_creatinine, calculated=True)
                self.user.ckd.baseline = baseline
            if self.user.ckd.value != True:
                self.user.ckd.value = True
                if baseline.eGFR_calculator():
                    if baseline.stage_calculator():
                        self.user.ckd.stage = baseline.stage_calculator()
            self.user.ckd.last_modified = "Behind the scenes"
            self.user.ckd.save()

    def diagnose_ckd(self):
        """
        Method that will determine if a user has CKD
        Checks for persistently abnormal renal function (eGFR) for 90 days or longer
        Any eGFR > 60 will result in a False return

        ***REQUIRES USER TO HAVE RACE, SEX, and AGE TO CALCULATE eGFR***
        Returns: Boolean, but modifies user.ckd first
        If True: will set user.ckd to True, assign user.ckd.baseline, set user.ckd.stage
                 will also set user.ckd.baseline.baseline to True
        If False: will set user.ckd to False, remove user.ckd.baseline/stage
                  will also set.user.ckd.baseline.baseline to False
        """
        baseline = self.get_baseline()

        def remove_ckd(self, creatinine=self):
            """
            Method that removes CKD and associated BaselineCreatinine
            Checks if the User has a BaselineCreatinine that was modified or created before the Creatinine calling the method
            Takes creatinine parameter, defaults to self.
            Creatinine can be set, such as when iterating over a list of Creatinines.

            Args:
                creatinine: Defaults to self.

            Returns:
                Bool: False if CKD removed, True if not
                Modified related models en route
            """
            # Check if there is a baseline that's not calculated (=User defined)
            # If so, check if the creatinine was drawn before the baseline was modified/created
            # If so, the Creatinine is older than the User-defined baseline, so don't manipulate it
            # If not, remove CKD, fields, and related BaselineCreatinine
            if baseline:
                if baseline.calculated == False:
                    if baseline.modified:
                        if baseline.modified < creatinine.date_drawn:
                            if self.user.ckd.value == True:
                                self.user.ckd.value = False
                                self.user.ckd.stage = None
                                self.user.ckd.last_modified = "Behind the scenes"
                                self.user.ckd.save()
                                baseline.delete()
                                return False
                    elif baseline.created < creatinine.date_drawn:
                        if self.user.ckd.value == True:
                            self.user.ckd.value = False
                            self.user.ckd.stage = None
                            self.user.ckd.last_modified = "Behind the scenes"
                            self.user.ckd.save()
                            baseline.delete()
                            return False
                return True
            else:
                if self.user.ckd.value == True:
                    self.user.ckd.value = False
                    self.user.ckd.stage = None
                    self.user.ckd.last_modified = "Behind the scenes"
                    self.user.ckd.save()
                return False

        # https://www.kidney-international.org/article/S0085-2538(15)50698-4/fulltext
        # Check if user has CKD already
        if self.user.ckd.value == True:
            if self.eGFR_calculator() > 60:
                return remove_ckd(self)
            else:
                self.set_baseline()
                return True
        # Assemble chronolocical list of creatinines, blank list of eGFRs
        creatinines = Creatinine.objects.filter(user=self.user).order_by("-date_drawn")
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
                return remove_ckd(self, creatinine=creatinine)
            # If eGFR is < 60
            else:
                # Check if list index is not the last item in the list
                # Check if subsequent eGFR is abnormal
                if eGFR_index < (len(eGFRs) - 1):
                    next_eGFR = eGFRs[eGFR_index + 1][0]
                    next_creatinine = eGFRs[eGFR_index + 1][1]
                    # If not, User does not have CKD, process Profile accordingly
                    if next_eGFR > 60:
                        return remove_ckd(self, creatinine=next_creatinine)
                    # If eGFR is again < 60
                    # Check if the current index's creatine.date_drawn is 90 days or more from the initial
                    else:
                        if creatinine.date_drawn - next_creatinine.date_drawn > timedelta(days=90):
                            # If all creatinines abnormal and 90 days or more apart, set_baseline
                            self.set_baseline()
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
            return self.value > (Decimal(var) * baseline.value)

        else:
            return self.value > (Decimal(var) * self.reference_upper)

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
        if self.diagnose_ckd() == True:
            # Try to fetch baseline
            self.baseline = self.get_baseline()
        # Check if Creatinine is a follow up on an abnormal
        if self.abnormal_followup:
            # Check if User has baseline Creatinine (=CKD)
            if self.baseline:
                if self.var_x_high(1.5, baseline=self.baseline):
                    return "urgent"
                elif self.var_x_high(1.25, baseline=self.baseline):
                    self.set_baseline()
                    return "nonurgent"
                else:
                    self.set_baseline()
            # If no baseline Creatinine
            else:
                if self.var_x_high(1.5):
                    return "urgent"
                elif self.var_x_high(1.25):
                    self.diagnose_ckd()
                    return "nonurgent"
                else:
                    self.diagnose_ckd()
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


class BasePlatelet(Lab):
    class Meta:
        abstract = True

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


class BaseWBC(Lab):
    class Meta:
        abstract = True

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


class BaseHemoglobin(Lab):
    class Meta:
        abstract = True

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


class BaselineALT(BaseALT):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name=("baselinealt_creator"),
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = "baseline_ALT"
    calculated = BooleanField(
        choices=BOOL_CHOICES,
        default=False,
    )
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
        if self.user.transaminitis.value != True:
            self.user.transaminitis.value = True
            self.user.transaminitis.save()


class BaselineAST(BaseAST):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name=("baselineast_creator"),
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = "baseline_AST"
    calculated = BooleanField(
        choices=BOOL_CHOICES,
        default=False,
    )
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
        if self.user.transaminitis.value != True:
            self.user.transaminitis.value = True
            self.user.transaminitis.save()


class ALT(BaseALT):
    # Creates date_drawn (=today) if not specified by form
    # Creates slug if not present
    def save(self, *args, **kwargs):
        if not self.id:
            if not self.date_drawn:
                self.date_drawn = timezone.now()
        super(ALT, self).save(*args, **kwargs)
        # Check if there isn't a slug
        if not self.slug:
            # If there isn't, check if there's a user
            if self.user:
                # If so, create slug from user and pk
                self.slug = slugify(self.user.username) + "-" + str(self.id)

    def get_AST(self):
        """
        Method that gets AST associated with ALT
        Fetches via date_drawn if available, otherwise created
        returns: AST object or None
        """
        # Check if ALT has AST
        if hasattr(self, "ast"):
            ast = self.ast
        # If not, check if ALT is a follow up for an abnormal lab
        elif self.abnormal_followup:
            # If so, check if the abnormal lab had an AST
            if hasattr(self.abnormal_followup, "ast"):
                ast = self.abnormal_followup.ast
            # Otherwise there's no AST
            else:
                ast = None
        else:
            ast = None
        return ast

    def normal_lfts(self):
        """
        Helper function that checks if an ALT has a normal associated AST
        If ALT is follow up on abnormal ALT, get_AST() will fetch AST from original abnormal
        If ALT and AST are both normal, returns True. False if not.
        Returns:
            Boolean: True if both normal, False if not
        """
        ast = self.get_AST()
        if ast:
            if ast.high == False:
                if self.high == False:
                    return True
        return False

    def get_baseline_AST(self):
        """
        Method that gets a User's baseline AST
        Returns: BaselineAST or none
        """
        return getattr(self.user, "baselineast", None)

    def set_baseline(self):
        """
        Method that sets a User's BaselineALT
        Also modifies User's Transaminitis to reflect BaselineALT
        ***WILL NOT MODIFY A USER-SET BASELINE (baseline.calculated == False)***

        Returns:
            Nothing or None, modifies related data
        """
        # Assemble list of ALTs for User
        ALTs = ALT.objects.filter(user=self.user).order_by("-date_drawn")
        # Filter the all_ALTs queryset to exclude values greater than 3 times the upper limit of normal
        # This will exclude episodes of acute hepatitis in the baseline calculation
        ALTs_all = []
        for alt in ALTs:
            if alt.var_x_high(self.user.patientprofile.lft_nonurgent) == False:
                ALTs_all.append(alt)
        # If no ALTs, return None
        if len(ALTs_all) == 0:
            return None
        # If 1 ALT, that must be the baseline
        if len(ALTs_all) == 1:
            baseline = self.get_baseline()
            # Check if there's a baseline
            if baseline:
                # If the baseline is User-entered, don't change it
                if baseline.calculated == False:
                    return None
                # If not, set baseline to only ALT
                else:
                    # Check if only ALT is greater than two years old, return None if so
                    if ALTs_all[0].date_drawn < timezone.now() - timedelta(days=730):
                        return None
                    baseline.value = ALTs_all[0].value
                    baseline.save()
                    self.user.transaminitis.last_modified = "Behind the scenes"
                    self.user.transaminitis.save()
            else:
                # Check if only ALT is greater than two years old, return None if so
                if ALTs_all[0].date_drawn < timezone.now() - timedelta(days=730):
                    return None
                baseline = BaselineALT.objects.create(user=self.user, value=ALTs[0].value, calculated=True)
                baseline.value = ALTs_all[0].value
                baseline.save()
                self.user.transaminitis.baseline_alt = baseline
                self.user.transaminitis.last_modified = "Behind the scenes"
                self.user.transaminitis.save()
        else:
            # Else assemble list of ALTs from t-180 > t-7 days
            # Based on method for establishing BaselineCreatinine
            # Adjusted for 6 month definition of chronic hepatitis
            ALTs = ALTs.filter(
                date_drawn__range=[
                    (timezone.now() - timedelta(days=180)),
                    timezone.now(),
                ]
            )
            # Filter the all_ALTs queryset to exclude values greater than 3 times the upper limit of normal
            # This will exclude episodes of acute hepatitis in the baseline calculation
            ALTs_lastsixmonths = []
            for alt in ALTs:
                if alt.var_x_high(self.user.patientprofile.lft_nonurgent) == False:
                    ALTs_lastsixmonths.append(alt)
            # If there are no ALTs over last 6 months, look back 1 year
            if len(ALTs_lastsixmonths) == 0:
                ALTs = ALT.objects.filter(
                    user=self.user,
                    date_drawn__range=[
                        (timezone.now() - timedelta(days=365)),
                        timezone.now(),
                    ],
                ).order_by("-date_drawn")
                # Filter the all_ALTs queryset to exclude values greater than 3 times the upper limit of normal
                # This will exclude episodes of acute hepatitis in the baseline calculation
                ALTs_lastyear = []
                for alt in ALTs:
                    if alt.var_x_high(self.user.patientprofile.lft_nonurgent) == False:
                        ALTs_lastyear.append(alt)
                # If there are no ALTs over last year, look back 2 years
                if len(ALTs_lastyear) == 0:
                    ALTs = ALT.objects.filter(
                        user=self.user,
                        date_drawn__range=[
                            (timezone.now() - timedelta(days=730)),
                            timezone.now(),
                        ],
                    ).order_by("-date_drawn")
                    # Filter the all_ALTs queryset to exclude values greater than 3 times the upper limit of normal
                    # This will exclude episodes of acute hepatitis in the baseline calculation
                    ALTs_lasttwoyears = []
                    for alt in ALTs:
                        if alt.var_x_high(self.user.patientprofile.lft_nonurgent) == False:
                            ALTs_lasttwoyears.append(alt)
                    # If no ALTs over last 2 years, return None
                    if len(ALTs_lasttwoyears) == 0:
                        return None
                    else:
                        ALTs = ALTs_lasttwoyears
                else:
                    ALTs = ALTs_lastyear
            else:
                ALTs = ALTs_lastsixmonths
            # Find mean over last year(s)
            mean_ALT = mean(alt.value for alt in ALTs)
            baseline = self.get_baseline()
            # Check if there's a baseline already
            if baseline:
                # If it's User-entered, don't change it
                if baseline.calculated == False:
                    return None
                # Otherwise set mean ALT to baseline
                else:
                    baseline.value = mean_ALT
                    baseline.save()
            # If no BaselineALT, create new one
            else:
                baseline = BaselineALT.objects.create(user=self.user, value=mean_ALT, calculated=True)
                # Set transaminitis baseline_alt to baseline, process, and save()
                self.user.transaminitis.baseline_alt = baseline
            self.user.transaminitis.last_modified = "Behind the scenes"
            self.user.transaminitis.save()

    def remove_transaminitis(self, alt=None):
        """
        Helper function that removes transaminitis and deletes related BaselineALT/AST models
        Sets User baselinealt and baselineast to None and saves User per Django delete() method
        ***DOES NOT CHECK 'NORMALCY' OF AST/ALT***
        ***RELIES ON ALT HAVING PASSED NORMAL_LFTS() METHOD***

        Args:
            alt: defaults to self

        Implicit Args:
            ast: will by definition be present by calling function:
            diagnose_transaminitis() --->>> normal_lfts())

        Returns:
            Bool: False if Transaminitis removed, True if not
            Modifies related models en route
        """
        # Fetch User's BaselineALT and BaselineAST if they exist
        baseline_alt = self.get_baseline()
        baseline_ast = self.get_baseline_AST()
        # Set alt to self if no argument declared in method call
        if alt == None:
            alt = self
        # Try to fetch ALT's 1to1 AST
        # Need to call on alt, not self, in case ALT was supplied as method arg
        ast = alt.get_AST()
        # Check if there is a BaselineALT
        if baseline_alt:
            # Check if BaselineALT is calculated
            if baseline_alt.calculated == False:
                # If not, check if BaselineALT was modified or created prior to:
                # ALT date_drawn > modified > created
                # If so, delete BaselineALT, set User.baselinealt to None
                # If not, BaselineALT is more recent, is User-entered
                # Don't modify User MedicalProfile in that context
                if hasattr(baseline_alt, "modified"):
                    baseline_alt_date = baseline_alt.modified
                elif hasattr(baseline_alt, "created"):
                    baseline_alt_date = baseline_alt.created
                else:
                    baseline_alt_date = None
                if hasattr(alt, "date_drawn"):
                    alt_date = alt.date_drawn
                elif hasattr(alt, "modified"):
                    alt_date = alt.modified
                elif hasattr(alt, "created"):
                    alt_date = alt.created
                else:
                    alt_date = None
                if baseline_alt_date and alt_date:
                    if baseline_alt_date < alt_date:
                        baseline_alt.delete()
                        self.user.baselinealt = None
                        self.user.save()
                        self.user.transaminitis.baseline_alt = None
                        self.user.transaminitis.last_modified = "Behind the scenes"
                        self.user.transaminitis.save()
            # If BaselineALT is calculated, delete it, set User.baselinealt to None
            else:
                baseline_alt.delete()
                self.user.baselinealt = None
                self.user.save()
                self.user.transaminitis.baseline_alt = None
                self.user.transaminitis.last_modified = "Behind the scenes"
                self.user.transaminitis.save()
        # If BaselienAST, process same as Baseline ALT above
        if baseline_ast:
            if baseline_ast.calculated == False:
                if hasattr(baseline_ast, "modified"):
                    baseline_ast_date = baseline_ast.modified
                elif hasattr(baseline_ast, "created"):
                    baseline_ast_date = baseline_ast.created
                else:
                    baseline_ast_date = None
                if hasattr(ast, "date_drawn"):
                    ast_date = ast.date_drawn
                elif hasattr(ast, "modified"):
                    ast_date = ast.modified
                elif hasattr(ast, "created"):
                    ast_date = ast.created
                else:
                    ast_date = None
                if baseline_ast_date and ast_date:
                    if baseline_ast_date < ast_date:
                        baseline_ast.delete()
                        self.user.baselineast = None
                        self.user.save()
                        self.user.transaminitis.baseline_ast = None
                        self.user.transaminitis.last_modified = "Behind the scenes"
                        self.user.transaminitis.save()
            else:
                baseline_ast.delete()
                self.user.baselineast = None
                self.user.save()
                self.user.transaminitis.baseline_alt = None
                self.user.transaminitis.last_modified = "Behind the scenes"
                self.user.transaminitis.save()
        # If there's no BaselineALT or BaselineAST, there isn't any transaminitis
        # Modify transaminitis fields and save(), return False
        if not hasattr(self.user, "baselinealt") and not hasattr(self.user, "baselineast"):
            if self.user.transaminitis.value == True:
                self.user.transaminitis.value = False
                self.user.transaminitis.save()
            return False
        else:
            return True

    def diagnose_transaminitis(self):
        """
        Method that will determine if a Patient has chronic transaminitis
        Checks for persistently abnormal liver function (ALT, AST) for 180 days or longer
        Any normal ALT/AST will result in False return

        Returns: Boolean, but modifies user.transaminitis first
        """

        # Assemble a list of all User's ALTs
        ALTs = ALT.objects.filter(
            user=self.user,
            date_drawn__range=[
                (timezone.now() - timedelta(days=730)),
                timezone.now(),
            ],
        ).order_by("-date_drawn")
        # Loop over all ALTs
        for alt_index in range(len(ALTs)):
            alt = ALTs[alt_index]
            # Check if each subsequent ALT normal
            if alt.normal_lfts() == True:
                # Remove transaminitis if so
                return self.remove_transaminitis(alt=alt)
            # Check if ALT is independently high (no AST to make normal_lfts() = True)
            elif alt.high == False:
                # Check if ALT has an associated high AST
                ast = alt.get_AST()
                if ast:
                    if ast.high == True:
                        # Check if there is at least 6 months from ALT and most recent abnormal ALT
                        if ALTs[0].date_drawn >= alt.date_drawn + timedelta(days=180):
                            # If so, set the baseline for transaminitis and return True
                            self.set_baseline()
                            return True
                # If there is no AST or no high AST:
                # There isn't enough info to determine LFTs are normal
                # So continue to iterate back over LFTs to see if transaminitis can be diagnosed
                continue
            # If ALT is abnormal
            else:
                # Check if there is at least 6 months from ALT and most recent abnormal ALT
                if ALTs[0].date_drawn >= alt.date_drawn + timedelta(days=180):
                    # If so, set the baseline for transaminitis and return True
                    self.set_baseline()
                    return True
                # If not 6 months, continue iteration
                else:
                    continue
        # Return False if 6 month span of abnormal LFTs not found
        # Do not call remove_transaminitis()
        # In case User is getting infrequent labs but does have chronic hepatitis
        # (Would be the case in a patient on stable-dose ULT)
        return False


class AST(BaseAST):
    alt = models.OneToOneField(ALT, on_delete=models.SET_NULL, blank=True, null=True)
    # Creates date_drawn (=today) if not specified by form
    # Creates slug if not present
    def save(self, *args, **kwargs):
        if not self.id:
            if not self.date_drawn:
                self.date_drawn = timezone.now()
        super(AST, self).save(*args, **kwargs)
        # Check if there isn't a slug
        if not self.slug:
            # If there isn't, check if there's a user
            if self.user:
                # If so, create slug from user and pk
                self.slug = slugify(self.user.username) + "-" + str(self.id)

    def get_ALT(self):
        """
        Method that gets ALT associated with AST
        Fetches via model instance if available
        Otherwise looks for whether AST is an abnormal F/U, checks original for associated ALT
        returns: AST object or None
        """
        # Check if AST has ALT
        if self.alt:
            alt = self.alt
        # If not, check if AST is a follow up for an abnormal lab
        elif self.abnormal_followup:
            # If so, check if the abnormal lab had an AST
            if self.abnormal_followup.alt:
                alt = self.abnormal_followup.alt
            # Otherwise there's no ALT
            else:
                alt = None
        else:
            alt = None
        return alt

    def normal_lfts(self):
        """
        Helper function that checks if an AST has a normal associated ALT
        If AST is follow up on abnormal AST, get_ALT() will fetch ALT from original abnormal
        If ALT and AST are both normal, returns True. False if not.
        Returns:
            Boolean: True if both normal, False if not
        """
        alt = self.get_ALT()
        if alt:
            if alt.high == False:
                if self.high == False:
                    return True
        return False

    def get_baseline_ALT(self):
        """
        Method that gets a User's baseline ALT
        Returns: BaselineALT or none
        """
        if hasattr(self.user, "baselinealt"):
            return self.user.baselinealt
        else:
            return None

    def set_baseline(self):
        """
        Method that sets a User's BaselineAST
        Also modifies User's Transaminitis to reflect BaselineAST
        ***WILL NOT MODIFY A USER-SET BASELINE (baseline.calculated == False)***

        Returns:
            Nothing or None, modifies related data
        """
        # Assemble list of ASTs for User
        ASTs = AST.objects.filter(user=self.user).order_by("-date_drawn")
        # Filter the all_ASTs queryset to exclude values greater than 3 times the upper limit of normal
        # This will exclude episodes of acute hepatitis in the baseline calculation
        ASTs_all = []
        for ast in ASTs:
            if ast.three_x_high == False:
                ASTs_all.append(ast)
        # If no ASTs, return None
        if len(ASTs_all) == 0:
            return None
        # If 1 AST, that must be the baseline
        if len(ASTs_all) == 1:
            solo_AST = ASTs_all[0]
            baseline = self.get_baseline()
            # Check if there's a baseline
            if baseline:
                # If the baseline is User-entered, don't change it
                if baseline.calculated == False:
                    return None
                # If not, set baseline to only AST
                else:
                    # Check if only AST is greater than two years old, return None if so
                    if solo_AST.date_drawn < timezone.now() - timedelta(days=730):
                        return None
                    # Otherwise set BaselineAST to the single AST value
                    baseline.value = solo_AST.value
                    baseline.save()
                    self.user.transaminitis.last_modified = "Behind the scenes"
                    self.user.transaminitis.save()
            # If there's no BaselineAST
            else:
                # Check if only AST is greater than two years old, return None if so
                if solo_AST.date_drawn < timezone.now() - timedelta(days=730):
                    return None
                # Otherwise create BaselineAST
                # Value equal to the only AST in ASTs_all
                baseline = BaselineAST.objects.create(user=self.user, value=solo_AST.value, calculated=True)
                baseline.value = solo_AST.value
                baseline.save()
                # Set Transaminitis to true, associate BaselineAST
                self.user.transaminitis.baseline_ast = baseline
                self.user.transaminitis.last_modified = "Behind the scenes"
                self.user.transaminitis.save()
        else:
            # Else assemble list of ASTs from t-180 days
            # Based on method for establishing BaselineCreatinine
            # Adjusted for 6 month definition of chronic hepatitis
            ASTs = ASTs.filter(
                date_drawn__range=[
                    (timezone.now() - timedelta(days=180)),
                    timezone.now(),
                ]
            )
            # Filter the ASTs queryset to exclude values greater than 3 times the upper limit of normal
            # This will exclude episodes of acute hepatitis in the baseline calculation
            ASTs_lastsixmonths = []
            for ast in ASTs:
                if ast.three_x_high == False:
                    ASTs_lastsixmonths.append(ast)
            # If there are no ASTs over last 6 months, look back 1 year
            if len(ASTs_lastsixmonths) == 0:
                ASTs = AST.objects.filter(
                    user=self.user,
                    date_drawn__range=[
                        (timezone.now() - timedelta(days=365)),
                        timezone.now(),
                    ],
                ).order_by("-date_drawn")
                # Filter the all_ASTs queryset to exclude values greater than 3 times the upper limit of normal
                # This will exclude episodes of acute hepatitis in the baseline calculation
                ASTs_lastyear = []
                for ast in ASTs:
                    if ast.three_x_high == False:
                        ASTs_lastyear.append(ast)
                # If there are no ASTs over last year, look back 2 years
                if len(ASTs_lastyear) == 0:
                    ASTs = AST.objects.filter(
                        user=self.user,
                        date_drawn__range=[
                            (timezone.now() - timedelta(days=730)),
                            timezone.now(),
                        ],
                    ).order_by("-date_drawn")
                    # Filter the all_ASTs queryset to exclude values greater than 3 times the upper limit of normal
                    # This will exclude episodes of acute hepatitis in the baseline calculation
                    ASTs_lasttwoyears = []
                    for ast in ASTs:
                        if ast.three_x_high == False:
                            ASTs_lasttwoyears.append(ast)
                    # If no ASTs over last 2 years, return None
                    if len(ASTs_lasttwoyears) == 0:
                        return None
                    else:
                        ASTs = ASTs_lasttwoyears
                else:
                    ASTs = ASTs_lastyear
            else:
                ASTs = ASTs_lastsixmonths
            # Find mean over last year(s)
            mean_AST = mean(ast.value for ast in ASTs)
            baseline = self.get_baseline()
            # Check if there's a baseline already
            if baseline:
                # If it's User-entered, don't change it
                if baseline.calculated == False:
                    return None
                # Otherwise set mean AST to baseline
                else:
                    baseline.value = mean_AST
                    baseline.save()
            # If no BaselineAST, create new one
            else:
                baseline = BaselineAST.objects.create(user=self.user, value=mean_AST, calculated=True)
                # Set transaminitis baseline_ast to baseline, process, and save()
                self.user.transaminitis.baseline_ast = baseline
            self.user.transaminitis.last_modified = "Behind the scenes"
            self.user.transaminitis.save()

    def remove_transaminitis(self, ast=None):
        """
        Helper function that removes transaminitis and deletes related BaselineALT/AST models
        Sets User baselinealt and baselineast to None and saves User per Django delete() method
        ***DOES NOT CHECK 'NORMALCY' OF AST/ALT***
        ***RELIES ON AST HAVING PASSED NORMAL_LFTS() METHOD***

        Args:
            ast: defaults to self

        Implicit Args:
            alt: will by definition be present by calling function:
            diagnose_transaminitis() --->>> normal_lfts())

        Returns:
            Bool: False if Transaminitis removed, True if not
            Modifies related models en route
        """
        # Fetch User's BaselineAST and BaselineALT if they exist
        baseline_ast = self.get_baseline()
        baseline_alt = self.get_baseline_ALT()
        # Set ast to self if no argument declared in method call
        if ast == None:
            ast = self
        # Try to fetch AST's 1to1 ALT
        # Need to call on ast, not self, in case AST was supplied as method arg
        alt = ast.get_ALT()
        # Check if there is a BaselineAST
        if baseline_ast:
            # Check if BaselineAST is calculated
            if baseline_ast.calculated == False:
                # If not, check if BaselineAST was modified or created prior to:
                # AST date_drawn > modified > created
                # If so, delete BaselineAST, set User.baselineast to None
                # If not, BaselineAST is more recent, is User-entered
                # Don't modify User MedicalProfile in that context
                if hasattr(baseline_ast, "modified"):
                    baseline_ast_date = baseline_ast.modified
                elif hasattr(baseline_ast, "created"):
                    baseline_ast_date = baseline_ast.created
                else:
                    baseline_ast_date = None
                if hasattr(ast, "date_drawn"):
                    ast_date = ast.date_drawn
                elif hasattr(ast, "modified"):
                    ast_date = ast.modified
                elif hasattr(ast, "created"):
                    ast_date = ast.created
                else:
                    ast_date = None
                if baseline_ast_date and ast_date:
                    if baseline_ast_date < ast_date:
                        baseline_ast.delete()
                        self.user.baselineast = None
                        self.user.save()
                        self.user.transaminitis.baseline_ast = None
                        self.user.transaminitis.last_modified = "Behind the scenes"
                        self.user.transaminitis.save()
            # If BaselineAST is calculated, delete it, set User.baselineast to None
            else:
                baseline_ast.delete()
                self.user.baselineast = None
                self.user.save()
                self.user.transaminitis.baseline_ast = None
                self.user.transaminitis.last_modified = "Behind the scenes"
                self.user.transaminitis.save()
        # If BaselineALT, process same as Baseline AST above
        if baseline_alt:
            if baseline_alt.calculated == False:
                if hasattr(baseline_alt, "modified"):
                    baseline_alt_date = baseline_alt.modified
                elif hasattr(baseline_alt, "created"):
                    baseline_alt_date = baseline_alt.created
                else:
                    baseline_alt_date = None
                if hasattr(alt, "date_drawn"):
                    alt_date = alt.date_drawn
                elif hasattr(alt, "modified"):
                    alt_date = alt.modified
                elif hasattr(alt, "created"):
                    alt_date = alt.created
                else:
                    alt_date = None
                if baseline_alt_date and alt_date:
                    if baseline_alt_date < alt_date:
                        baseline_alt.delete()
                        self.user.baselinealt = None
                        self.user.save()
                        self.user.transaminitis.baseline_alt = None
                        self.user.transaminitis.last_modified = "Behind the scenes"
                        self.user.transaminitis.save()
            else:
                baseline_alt.delete()
                self.user.baselinealt = None
                self.user.save()
                self.user.transaminitis.baseline_ast = None
                self.user.transaminitis.last_modified = "Behind the scenes"
                self.user.transaminitis.save()
        # If there's no BaselineALT or BaselineAST, there isn't any transaminitis
        # Modify transaminitis fields and save(), return False
        if not hasattr(self.user, "baselinealt") and not hasattr(self.user, "baselineast"):
            if self.user.transaminitis.value == True:
                self.user.transaminitis.value = False
                # Need to change last_modified again here in the event that Transaminitis is removed but no BaselineALT/AST is removed above
                self.user.transaminitis.last_modified = "Behind the scenes"
                self.user.transaminitis.save()
            return False
        else:
            return True

    def diagnose_transaminitis(self):
        """
        Method that will determine if a Patient has chronic transaminitis
        Checks for persistently abnormal liver function (ALT, AST) for 180 days or longer
        Any normal ALT/AST will result in False return

        Returns: Boolean, but modifies user.transaminitis first
        """

        # Assemble a list of all User's ASTs over last 2 years
        ASTs = AST.objects.filter(
            user=self.user,
            date_drawn__range=[
                (timezone.now() - timedelta(days=730)),
                timezone.now(),
            ],
        ).order_by("-date_drawn")
        # Loop over all ASTs
        for ast_index in range(len(ASTs)):
            ast = ASTs[ast_index]
            # Check if each subsequent AST normal
            if ast.normal_lfts() == True:
                # Remove transaminitis if so
                return self.remove_transaminitis(ast=ast)
            # Check if AST is independently high (no ALT to make normal_lfts() = True)
            elif ast.high == False:
                # Check if AST has an associated high ALT
                alt = ast.get_ALT()
                if alt:
                    if alt.high == True:
                        # Check if there is at least 6 months from AST and most recent abnormal AST
                        if ASTs[0].date_drawn >= ast.date_drawn + timedelta(days=180):
                            # If so, set the baseline for transaminitis and return True
                            self.set_baseline()
                            return True
                # If there is no ALT or no high ALT:
                # There isn't enough info to determine LFTs are normal
                # So continue to iterate back over LFTs to see if transaminitis can be diagnosed
                continue
            # If AST is abnormal
            else:
                # Check if there is at least 6 months from AST and most recent abnormal AST
                if ASTs[0].date_drawn >= ast.date_drawn + timedelta(days=180):
                    # If so, set the baseline for transaminitis and return True
                    self.set_baseline()
                    return True
                # If not 6 months, continue iteration
                else:
                    continue
        # Return False if 6 month span of abnormal LFTs not found
        # Do not call remove_transaminitis()
        # In case User is getting infrequent labs but does have chronic hepatitis
        # (Would be the case in a patient on stable-dose ULT)
        return False


class Platelet(BasePlatelet):
    # Creates date_drawn (=today) if not specified by form
    # Creates slug if not present
    def save(self, *args, **kwargs):
        if not self.id:
            if not self.date_drawn:
                self.date_drawn = timezone.now()
        super(Platelet, self).save(*args, **kwargs)
        # Check if there isn't a slug
        if not self.slug:
            # If there isn't, check if there's a user
            if self.user:
                # If so, create slug from user and pk
                self.slug = slugify(self.user.username) + "-" + str(self.id)

    def set_baseline(self):
        """
        Method that sets a User's BaselinePlatelet value
        """
        baseline = self.get_baseline()

        platelets = Platelet.objects.filter(user=self.user).order_by("-date_drawn")
        # If no Platelets, return None
        if len(platelets) == 0:
            return None
        # If 1 Platelet, that must be the baseline
        if len(platelets) == 1:
            solo_platelet = platelets[0]
            baseline = self.get_baseline()
            # Check if there's a baseline
            if baseline:
                # If the baseline is User-entered, don't change it
                if baseline.calculated == False:
                    return None
                # If not, set baseline to only Platelet
                else:
                    # Check if only Platelet is greater than two years old, return None if so
                    if solo_platelet.date_drawn < timezone.now() - timedelta(days=730):
                        return None
                    # Otherwise set BaselinePlatelet to the single Platelet value
                    baseline.value = solo_platelet.value
                    baseline.save()
                    return baseline
            # If there's no BaselinePlatelet
            else:
                # Check if only Platelet is greater than two years old, return None if so
                if solo_platelet.date_drawn < timezone.now() - timedelta(days=730):
                    return None
                # Otherwise create BaselinePlatelet
                # Value equal to the only Platelet
                baseline = BaselinePlatelet.objects.create(user=self.user, value=solo_platelet.value, calculated=True)
                # Return the BaselinePlatelet so it can be set to User's Thrombocytopenia/cytosis via their respective diagnose() methods
                return baseline
        else:
            # Else assemble list of Platelets from t-180 days
            # Not based on any formal methodology (I couldn't find any)
            platelets = platelets.filter(
                date_drawn__range=[
                    (timezone.now() - timedelta(days=180)),
                    timezone.now(),
                ]
            )
            # If there are no Platelets over last 6 months, look back 1 year
            if len(platelets) == 0:
                platelets = Platelet.objects.filter(
                    user=self.user,
                    date_drawn__range=[
                        (timezone.now() - timedelta(days=365)),
                        timezone.now(),
                    ],
                ).order_by("-date_drawn")
                # If there are no Platelets over last year, look back 2 years
                if len(platelets) == 0:
                    platelets = Platelet.objects.filter(
                        user=self.user,
                        date_drawn__range=[
                            (timezone.now() - timedelta(days=730)),
                            timezone.now(),
                        ],
                    ).order_by("-date_drawn")
                    # If no Platelets over last 2 years, return None
                    if len(platelets) == 0:
                        return None
            # Find mean over last 6 months / year(s)
            # Need to call ceil() to produce an integer and ensure consistent behavior
            mean_platelet = ceil(mean(platelet.value for platelet in platelets))
            # Check if there's a baseline already
            if baseline:
                # If it's User-entered, don't change it
                if baseline.calculated == False:
                    return None
                # Otherwise set mean Platelet to baseline
                else:
                    baseline.value = mean_platelet
                    baseline.save()
                    return baseline
            # If no BaselinePlatelet, create new one
            else:
                baseline = BaselinePlatelet.objects.create(user=self.user, value=mean_platelet, calculated=True)
                # Return the BaselinePlatelet so it can be set to User's Thrombocytopenia/cytosis via their respective diagnose() methods
                return baseline

    def remove_thrombocytopenia(self):
        """
        Method that changes User's Thrombocytopenia.value to False
        Deletes User's BaselinePlatelet object
        returns: False if thrombocytopenia removed, True if not
        """
        # Fetch User's BaselienPlatelet
        baseline = self.get_baseline()

        # If User has BaselinePlatelet
        if baseline:
            # If BaselinePlatelet is set by User
            if baseline.low and baseline.calculated == False:
                # Compare BaselinePlatelet.modified>created to >>>
                # Platelet.date_drawn>modified>created
                if hasattr(baseline, "modified"):
                    baseline_date = baseline.modified
                elif hasattr(baseline, "created"):
                    baseline_date = baseline.created
                else:
                    baseline_date = None
                if hasattr(self, "date_drawn"):
                    platelet_date = self.date_drawn
                elif hasattr(self, "modified"):
                    platelet_date = self.modified
                elif hasattr(self, "created"):
                    platelet_date = self.created
                else:
                    platelet_date = None
                # If there is a BaselinePlatelet date and Platelet date, compare
                if baseline_date and platelet_date:
                    # If Platelet date newer than BaselinePlatelet date >>>
                    # Remove BaselinePlatelet
                    if baseline_date < platelet_date:
                        baseline.delete()
                        self.user.baselineplatelet = None
                        self.user.save()
                        self.user.thrombocytopenia.baseline = None
                        self.user.thrombocytopenia.last_modified = "Behind the scenes"
                        self.user.thrombocytopenia.save()
            # If BaselinePlatelet is calculated, remove it
            elif baseline.low:
                baseline.delete()
                self.user.baselineplatelet = None
                self.user.save()
                self.user.thrombocytopenia.baseline = None
                self.user.thrombocytopenia.last_modified = "Behind the scenes"
                self.user.thrombocytopenia.save()
        # If there's no BaselinePlatelet >>>
        # Modify thrombocytopenia fields, save(), and return False
        if hasattr(self.user, "baselineplatelet") == False:
            if self.user.thrombocytopenia.value == True:
                self.user.thrombocytopenia.value = False
                self.user.thrombocytopenia.save()
            return False
        # Else return True
        else:
            return True

    def diagnose_thrombocytopenia(self):
        """
        Method that un/diagnoses a User's Thrombocytopenia
        Changes Thrombocytopenia.value to True/False
        Sets or removes BaselinePlatelet value via >>>
        set_baseline() or remove_thrombocytopenia() methods

        """
        # Assemble a list of all User's Platelets
        platelets = Platelet.objects.filter(
            user=self.user,
            date_drawn__range=[
                (timezone.now() - timedelta(days=730)),
                timezone.now(),
            ],
        ).order_by("-date_drawn")
        # Loop over all Platelets
        for platelet_index in range(len(platelets)):
            platelet = platelets[platelet_index]
            # If value wasn't low, call remove_thrombocytopenia()
            if platelet.low == False:
                return platelet.remove_thrombocytopenia()
            else:
                # If Platelets are 3 months apart and continuously low >>>
                if platelets[0].date_drawn >= platelet.date_drawn + timedelta(days=90):
                    # set BaselinePlatelet
                    # Modify Thrombocytopenia to True
                    baseline = self.set_baseline()
                    # Check if Baseline isn't None (for instance, with User-set BaselinePlatelet)
                    if baseline:
                        self.user.thrombocytopenia.value = True
                        self.user.thrombocytopenia.last_modified = "Behind the scenes"
                        self.user.thrombocytopenia.baseline = baseline
                        self.user.thrombocytopenia.save()
                    return True
                # If not, keep iterating back in time (through the list)
                continue
        # If no Platelets continuously low 3 months apart, return False
        return False

    def remove_thrombocytosis(self):
        """
        Method that changes User's Thrombocytosis.value to False
        Deletes User's BaselinePlatelet object
        returns: False if thrombocytosis removed, True if not
        """
        # Fetch User's BaselienPlatelet
        baseline = self.get_baseline()

        # If User has BaselinePlatelet
        if baseline:
            # If BaselinePlatelet is set by User
            if baseline.calculated == False:
                # Compare BaselinePlatelet.modified>created to >>>
                # Platelet.date_drawn>modified>created
                if hasattr(baseline, "modified"):
                    baseline_date = baseline.modified
                elif hasattr(baseline, "created"):
                    baseline_date = baseline.created
                else:
                    baseline_date = None
                if hasattr(self, "date_drawn"):
                    platelet_date = self.date_drawn
                elif hasattr(self, "modified"):
                    platelet_date = self.modified
                elif hasattr(self, "created"):
                    platelet_date = self.created
                else:
                    platelet_date = None
                # If there is a BaselinePlatelet date and Platelet date, compare
                if baseline_date and platelet_date:
                    # If Platelet date newer than BaselinePlatelet date >>>
                    # Remove BaselinePlatelet
                    if baseline_date < platelet_date:
                        baseline.delete()
                        self.user.baselineplatelet = None
                        self.user.save()
                        self.user.thrombocytosis.baseline = None
                        self.user.thrombocytosis.last_modified = "Behind the scenes"
                        self.user.thrombocytosis.save()
            # If BaselinePlatelet is calculated, remove it
            else:
                baseline.delete()
                self.user.baselineplatelet = None
                self.user.save()
                self.user.thrombocytosis.baseline = None
                self.user.thrombocytosis.last_modified = "Behind the scenes"
                self.user.thrombocytosis.save()
        # If there's no BaselinePlatelet >>>
        # Modify thrombocytosis fields, save(), and return False
        if hasattr(self.user, "baselineplatelet") == False:
            if self.user.thrombocytosis.value == True:
                self.user.thrombocytosis.value = False
                self.user.thrombocytosis.save()
            return False
        # Else return True
        else:
            return True

    def diagnose_thrombocytosis(self):
        """
        Method that un/diagnoses a User's Thrombocytosis
        Changes Thrombocytosis.value to True/False
        Sets or removes BaselinePlatelet value via >>>
        set_baseline() or remove_thrombocytosis() methods

        """
        # Assemble a list of all User's Platelets for last 2 years
        platelets = Platelet.objects.filter(
            user=self.user,
            date_drawn__range=[
                (timezone.now() - timedelta(days=730)),
                timezone.now(),
            ],
        ).order_by("-date_drawn")
        # Loop over all Platelets
        for platelet_index in range(len(platelets)):
            platelet = platelets[platelet_index]
            # If value wasn't low, call remove_thrombocytosis()
            if platelet.high == False:
                return platelet.remove_thrombocytosis()
            else:
                # If Platelets are 3 months apart and continuously high >>>
                if platelets[0].date_drawn >= platelet.date_drawn + timedelta(days=90):
                    # set BaselinePlatelet
                    # Modify Thrombocytosis to True
                    baseline = self.set_baseline()
                    # Check if Baseline isn't None (for instance, with User-set BaselinePlatelet)
                    if baseline:
                        self.user.thrombocytosis.value = True
                        self.user.thrombocytosis.last_modified = "Behind the scenes"
                        self.user.thrombocytosis.baseline = baseline
                        self.user.thrombocytosis.save()
                    return True
                # If not, keep iterating back in time (through the list)
                continue
        # If no Platelets continuously high 3 months apart, return False
        return False

    def process_high(self):
        """
        Function that processes a high Platelet.
        Will diagnose Thrombocytosis via diagnose_thrombocytosis() method.
        Checks if this object is a follow up an abnormal Platelet.
        Never returns "nonurgent", "urgent", or "emergency" or stop ULTPlan.
        Returns "trivial" for elevation or "error".

        Returns:
            string or nothing: returns "trivial", "error" or None
        """
        # Assign trivial % to process high Platelet
        # Pulled from PatientProfile
        trivial = self.user.patientprofile.platelet_high_trivial
        nonurgent = self.user.patientprofile.platelet_high_nonurgent
        urgent = self.user.patientprofile.platelet_high_urgent
        emergency = self.user.patientprofile.platelet_high_emergency

        # Call diagnose_thrombocytosis, will set BaselinePlatelet if appropriate
        self.diagnose_thrombocytosis()
        # If BaselinePlatelet set above, var_x_high will use it for processing
        if self.var_x_high(trivial):
            self.flag = 1
            self.action = 0
            self.save()
        return self.show_action

    def process_low(self):
        """
        Function that processes a low Platelet.
        Will diagnose Thrombocytopenia via diagnose_thrombocytopenia() method.
        Checks if this object is a follow up an abnormal Platelet.
        Can return "trivial, "nonurgent", "urgent", or "emergency", the latter 2 will stop ULTPlan.
        If low Platelet is an abnormal follow up, processes differently.
        Returns:
            string or nothing: string is one of the Flag options
        """
        # Assign trivial % to process low Platelet
        # Pulled from PatientProfile
        trivial = self.user.patientprofile.platelet_low_trivial
        nonurgent = self.user.patientprofile.platelet_low_nonurgent
        urgent = self.user.patientprofile.platelet_low_urgent
        emergency = self.user.patientprofile.platelet_low_emergency

        # Call diagnose_thrombocytosis, will set BaselinePlatelet if appropriate
        self.diagnose_thrombocytosis()
        # If BaselinePlatelet set above, var_x_high will use it for processing
        # If Platelet is a follow up on an abnormal Platelet
        if self.abnormal_followup:
            if self.abnormal_followup.flag == 3:
                if self.var_x_high(urgent):
                    # 2 urgent low platelets in a row should flag emergency
                    self.flag = 4
                    self.action = 5
                    self.save()
                elif self.var_x_high(trivial):
                    # If urgent then trivial or nonurgent, low Platelet is improving
                    self.flag = 7
                    self.action = 0
                    self.save()
                else:
                    # If urgent then normal, it was probably an error
                    self.flag = 5
                    self.action = 0
                    self.save()
                # Return self.action for processing
                return self.action
            elif self.abnormal_followup.flag == 2:
                if self.var_x_high(urgent):
                    # 2 urgent low platelets in a row should flag emergency
                    self.flag = 4
                    self.action = 5
                    self.save()
            elif self.abnormal_followup.flag == 6:

            elif self.abnormal_followup.flag = 7:


            # If follow-up Platelet at or below User's baseline, the original abnormality was likely an error
            if self.var_x_high(trivial) == False:
                self.flag = 5
                self.action = 0
                self.save()
                # Return at end of method (None)
            # If follow-up is 50% the baseline or lower limit of normal: Platelet is still very low and/or getting worse
            if self.var_x_high(urgent):
                # If getting worse or at emergency level, trigger emergency
                if self.abnormal_followup.flag == 2 or self.var_x_high(emergency) or self.value < 10:
                    self.flag = 4
                    self.action = 5
                    self.save()
                    return self.show_flag
                # Otherwise the abnormal lab was also "urgent" and the Platelet value is stable
                else:
                    self.flag = 9
                    self.save()
                    return "stable_restart"
            # If abnormal_followup was not urgent, it must have been nonurgent
            else:
                # If initial Platelet was "urgent" and now is not, must be improving and
                if self.abnormal_followup.flag == 3:
                    self.flag = 6
                    self.save()
                    return "improving_restart"
                elif self.var_x_high(nonurgent):
                    self.flag = 8
                    self.save()
                    return "stable_continue"
                else:
                    self.flag = 6
                    self.save()
                    return "improving_continue"

        # If Platelet isn't a follow up on an abnormal Platelet
        else:
            # Emergency values will not flag a follow up Platelet check
            # Will instead recommend User seek medical attention
            # Emergency Pause ULTPlan (will have to be removed by Provider or User)
            if self.var_x_low(emergency) or self.value < 10:
                self.flag = 4
                self.action = 4
                self.save()
            # Urgent values will prompt a recheck
            elif self.var_x_low(urgent):
                self.flag = 3
                self.action = 1
                self.save()
            elif self.var_x_low(nonurgent):
                self.flag = 2
                self.action = 0
                self.save()
            elif self.var_x_low(trivial):
                self.flag = 1
                self.action = 0
                self.save()
            return self.action


class BaselinePlatelet(BasePlatelet):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name=("baselineplatelet_creator"),
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = "baseline_platelet"
    calculated = BooleanField(
        choices=BOOL_CHOICES,
        default=False,
    )
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


class WBC(BaseWBC):
    # Creates date_drawn (=today) if not specified by form
    # Creates slug if not present
    def save(self, *args, **kwargs):
        if not self.id:
            if not self.date_drawn:
                self.date_drawn = timezone.now()
        super(WBC, self).save(*args, **kwargs)
        # Check if there isn't a slug
        if not self.slug:
            # If there isn't, check if there's a user
            if self.user:
                # If so, create slug from user and pk
                self.slug = slugify(self.user.username)


class BaselineWBC(BaseWBC):

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name=("baselinewbc_creator"),
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = "baseline_WBC"
    calculated = BooleanField(
        choices=BOOL_CHOICES,
        default=False,
    )
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


class Hemoglobin(BaseHemoglobin):
    # Creates date_drawn (=today) if not specified by form
    # Creates slug if not present
    def save(self, *args, **kwargs):
        if not self.id:
            if not self.date_drawn:
                self.date_drawn = timezone.now()
        super(Hemoglobin, self).save(*args, **kwargs)
        # Check if there isn't a slug
        if not self.slug:
            # If there isn't, check if there's a user
            if self.user:
                # If so, create slug from user and pk
                self.slug = slugify(self.user.username)


class BaselineHemoglobin(BaseHemoglobin):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name=("baselinehemoglobin_creator"),
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = "baseline_hemoglobin"
    calculated = BooleanField(
        choices=BOOL_CHOICES,
        default=False,
    )
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


class Creatinine(BaseCreatinine):
    name = "creatinine"
    # Creates a date_drawn (=today) if not specified by form
    # Creates slug if not present
    def save(self, *args, **kwargs):
        if not self.id:
            if not self.date_drawn:
                self.date_drawn = timezone.now()
        super(Creatinine, self).save(*args, **kwargs)
        # Check if there isn't a slug
        if not self.slug:
            # If there isn't, check if there's a user
            if self.user:
                # If so, create slug from user and pk
                self.slug = slugify(self.user.username) + "-" + str(self.id)


class BaselineCreatinine(BaseCreatinine):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name=("baselinecreatinine_creator"),
    )
    name = "baseline_creatinine"
    calculated = BooleanField(
        choices=BOOL_CHOICES,
        default=False,
    )
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
    abnormal_followup = models.OneToOneField("self", on_delete=models.CASCADE, null=True, blank=True, default=None)
    due = models.DateTimeField(
        help_text="When is this lab check due?",
        default=(timezone.now() + timedelta(days=42)),
    )
    completed = models.BooleanField(choices=BOOL_CHOICES, help_text="Is this lab check completed?", default=False)
    completed_date = models.DateTimeField(
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
        """
        Checks if a LabCheck is delinquently overdue
        Used to pause ULTPlan

        Returns: Boolean, True is delinquent, False if not
        """
        return timezone.now() >= self.due - self.ultplan.delinquent_lab_interval

    @property
    def overdue(self):
        """
        Checks if the LabCheck is overdue
        Returns: Boolean, True if overdue, False if not
        """
        return timezone.now() >= self.due

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

    def get_labcheck(self):
        """
        Method that gets LabCheck associated with LabCheck
        self will be 1to1 with LabCheck.abnormal_followup
        returns: LabCheck object or None
        """
        # Check if Lab has LabCheck
        return getattr(self, "labcheck", None)

    def __str__(self):
        if self.completed == True:
            return f"{str(self.user).capitalize()}'s lab check completed {self.completed_date}"
        else:
            return f"{str(self.user).capitalize()}'s lab check due {self.due}"

    def get_absolute_url(self):
        return reverse("ultplan:detail", kwargs={"slug": self.ultplan.slug})
