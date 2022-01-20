from datetime import datetime, timedelta, timezone

from django.conf import settings
from django.db import models
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel
from simple_history.models import HistoricalRecords

from ..lab.models import (
    ALT,
    AST,
    WBC,
    Creatinine,
    Hemoglobin,
    LabCheck,
    Platelet,
    Urate,
)
from .choices import BOOL_CHOICES


class ULTPlan(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    dose_adjustment = models.IntegerField(
        help_text="What is the dose adjustment for each titration for the chosen medication?",
        verbose_name="Dose Adjustment",
        default=100,
    )
    goal_urate = models.FloatField(help_text="What is the goal uric acid?", verbose_name="Goal Uric Acid", default=6.0)
    titration_lab_interval = models.DurationField(
        help_text="How frequently are labs required to be checked duration ULT titration?",
        verbose_name="Titration Lab Check Interval",
        default=timedelta(days=42),
    )
    monitoring_lab_interval = models.DurationField(
        help_text="How frequently are labs required to be checked during routine monitoring?",
        verbose_name="Monitoring Lab Check Interval",
        default=timedelta(days=180),
    )
    urgent_lab_interval = models.DurationField(
        help_text="How frequently do you recheck urgent labs?",
        verbose_name="Urgent Lab Check Interval",
        default=timedelta(days=14),
    )
    titrating = models.BooleanField(
        choices=BOOL_CHOICES, help_text="Is this ULTPlan still in the titration phase?", default=True
    )
    last_titration = models.DateField(help_text="When was the ULT dose last titrated?", null=True, blank=True)
    pause = models.BooleanField(choices=BOOL_CHOICES, help_text="Is this ULTPlan on pause?", default=False)
    history = HistoricalRecords()

    def last_labcheck(self):
        """Function that fetches the last LabCheck for the ULTPlan

        Returns:
            [object]: [LabCheck]
        """
        try:
            self.labcheck = self.labcheck_set.order_by("created").last()
        except:
            self.labcheck = None
        if self.labcheck:
            return self.labcheck
        else:
            return None

    def last_completed_labcheck(self):
        """Function that fetches the last completed LabCheck for the ULTPlan

        Returns:
            [object]: [LabCheck]
        """
        try:
            self.labcheck = self.labcheck_set.filter(completed=True).order_by("created").last()
        except:
            self.labcheck = None
        if self.labcheck:
            return self.labcheck
        else:
            return None

    def lab_status(self, Lab):
        """Function that takes a Lab model as an argument and looks whether an instance of that Lab is due in the most recent (last()) LabCheck model instance for the ULTPlan

        Returns:
            [boolean]: [Returns True if ALT is due, False if not]
        """
        # Get last LabCheck for ULTPlan using last_labcheck() function
        self.labcheck = self.last_labcheck()
        # Try to get last associated Lab instance, return None if not present
        try:
            self.lab = Lab.objects.get(labcheck=self.labcheck)
        except:
            self.lab = None
        # If Lab instance is None, check if it is due, return True if so, False if not
        if self.lab == None:
            if (self.labcheck.due - timedelta(days=7)) <= datetime.today().date():
                due = True
            else:
                due = False
        # If Lab instance is not None, it is present and thus isn't due
        else:
            due = False
        return due

    def labs_due(self):
        """Function that checks the lab_status for each of the LabCheck labs and returns a string of Labs that are overdue

        Returns:
            str: of overdue Labs for LabCheck
        """
        if (
            self.lab_status(ALT) == False
            and self.lab_status(AST) == False
            and self.lab_status(Creatinine) == False
            and self.lab_status(Hemoglobin) == False
            and self.lab_status(Platelet) == False
            and self.lab_status(WBC) == False
            and self.lab_status(Urate) == False
        ):
            return "none"
        else:
            overdue_labs = []
            if self.lab_status(ALT) == True:
                overdue_labs.append("ALT")
            if self.lab_status(AST) == True:
                overdue_labs.append("AST")
            if self.lab_status(Creatinine) == True:
                overdue_labs.append("creatinine")
            if self.lab_status(Hemoglobin) == True:
                overdue_labs.append("hemoglobin")
            if self.lab_status(Platelet) == True:
                overdue_labs.append("platelets")
            if self.lab_status(WBC) == True:
                overdue_labs.append("WBC")
            if self.lab_status(Urate) == True:
                overdue_labs.append("urate")
            overdue_labs_string = ""
            if len(overdue_labs) > 1:
                for i in range(len(overdue_labs) - 1):
                    overdue_labs_string += overdue_labs[i]
                    overdue_labs_string += ", "
                overdue_labs_string += overdue_labs[len(overdue_labs) - 1]
            else:
                overdue_labs_string += overdue_labs[0]
            return overdue_labs_string

    def labcheck_due(self):
        """Model method that determines if the most recent LabCheck for the ULTPlan is due, returns False if not"""
        try:
            self.labcheck = self.labcheck_set.last()
        except:
            self.labcheck = None
        if self.labcheck == None:
            return True
        elif self.labcheck.completed == False:
            if (
                (self.labcheck.due + timedelta(days=7))
                >= datetime.today().date()
                >= (self.labcheck.due - timedelta(days=7))
            ):
                return True
            else:
                return False
        else:
            return False

    def get_ult(self):
        """
        Returns ULTPlan associated ULT (allopurinol, febuxostat, probenecid)
        returns:
        object: ULT Treatment object
        """
        try:
            allopurinol = self.allopurinol
        except:
            allopurinol = None
        try:
            febuxostat = self.febuxostat
        except:
            febuxostat = None
        try:
            probenecid = self.probenecid
        except:
            probenecid = None
        if allopurinol:
            return allopurinol
        if febuxostat:
            return febuxostat
        if probenecid:
            return probenecid
        else:
            return "No ULT!!!"

    def get_ppx(self):
        """
        Returns ULTPlan associated PPx (colchicine, ibuprofen, naproxen, or prednisone)
        returns:
        object: PPx Treatment
        """
        try:
            colchicine = self.colchicine
        except:
            colchicine = None
        try:
            ibuprofen = self.ibuprofen
        except:
            ibuprofen = None
        try:
            naproxen = self.naproxen
        except:
            naproxen = None
        try:
            prednisone = self.prednisone
        except:
            prednisone = None
        if colchicine:
            return colchicine
        if ibuprofen:
            return ibuprofen
        if naproxen:
            return naproxen
        if prednisone:
            return prednisone
        else:
            return "No PPx!!!"

    def titrate(self, labcheck):
        """
        Method that takes a LabCheck as an argument and is called when that LabCheck is successfully updated by LabCheckUpdate view.
        Checks whether or not to titrate associated ULT based off Lab values.
        Returns:
        boolean = True if anything was changed, False if not. Also modifies related models in the process.
        """

        def six_months_at_goal(labcheck_list, goal_urate, r):
            """Recursive function that takes a list of LabChecks, ordered by their completed_date, and a goal_urate as arguments.
            Returns True if there is a 6 or greater month period where the current and all other preceding Urates were < goal_urate.
            Must contain at least Urate values at least 6 months apart."""
            # If index + r is greater than the length of the list, the recursion has run beyond the end of the list and has not found a 6 month period where > 1 Urates were < goal_urate, thus returns False
            if r > len(labcheck_list):
                return False
            # Check if urate at LabCheck[r] is under goal_urate
            if labcheck_list[r].urate.value < goal_urate:
                # If so, check if urate at LabCheck[r] is greater than 6 months apart from current urate at LabCheck[0]
                # Need to use completed_date, not created from TimeStampedModel, as the latter is overwritten at model creation. completed_date set by LabCheckUpdate view form_valid()
                if labcheck_list[0].completed_date - labcheck_list[r].completed_date > timedelta(days=180):
                    return True
                # If LabChecks aren't 6 months apart but both are below goal_urate, recurse to the next urate further back in time LabCheck[r+1]
                else:
                    return six_months_at_goal(labcheck_list, goal_urate, r + 1)
            # If Urate hasn't been under goal_urate for at least 6 months with greater 2 or more observations, return False
            else:
                return False

        def create_labcheck(self):
            """Method that checks if ULTPLan titrating attribute is False, if so creates the next LabCheck monitoring_lab_interval days into the future.
            Otherwise sets it titration_lab_interval days into the future.
            returns: nothing
            """
            # If User's ULTPlan is no longer titrating, create LabCheck for monitoring further into the future
            if self.titrating == False:
                LabCheck.objects.create(
                    user=self.user,
                    ultplan=self,
                    due=datetime.today().date() + self.monitoring_lab_interval,
                )
            # If User's ULTPlan is still titrating (titrating == True), create LabCheck for continued titration lab monitoring
            else:
                LabCheck.objects.create(
                    user=self.user,
                    ultplan=self,
                    due=(datetime.today().date() + self.titration_lab_interval),
                )

        if labcheck.completed == True:
            # If the LabCheck is completed, fetch ULT, dose_adjustment, PPx, and all LabChecks for ULTPlan
            self.ult = self.get_ult()
            self.dose_adjustment = self.dose_adjustment
            self.ppx = self.get_ppx()
            self.labchecks = self.labcheck_set.all().order_by("-completed_date")

            if len(self.labchecks) == 1:
                # If there is only 1 LabCheck for ULTPlan, it is the first and no titration will be performed
                # Call create_labcheck() to create the next LabCheck that's due
                create_labcheck(self)
                return False
            if labcheck.urate.value <= self.goal_urate:
                # If LabCheck urate is less than ULTPlan goal, check if urate has been under 6.0 for 6 months or longer in order to determine whether or not to discontinue PPx
                if len(self.labchecks) > 1:
                    # If six_months_at_goal returns False, no titration performed, maintain the status quo for treatment
                    if six_months_at_goal(self.labchecks, self.goal_urate, 1) == False:
                        # Call create_labcheck() to create the next LabCheck that's due
                        create_labcheck(self)
                        return False
                    # If six_months_at_Goal returns True, titration is performed,
                    elif six_months_at_goal(self.labchecks, self.goal_urate, 1) == True:
                        # Prophylaxis no longer required, add date_ended to today(), switch prophylaxis_finished to True, and save PPx
                        self.ppx.date_ended = datetime.today().date()
                        self.ppx.prophylaxis_finished = True
                        self.ppx.save()
                        # Switch titration to False as titration is finished, add last_titration date to today()
                        self.titrating = False
                        self.last_titration = datetime.today().date()
                        # Call create_labcheck() to create the next LabCheck that's due
                        create_labcheck(self)
                        return True
            elif labcheck.urate.value > self.goal_urate:
                # If LabCheck uric acid is higher than goal, increase ult.dose by ULTPlan dose_adjustment and save ult
                self.ult.dose = self.ult.dose + self.dose_adjustment
                self.ult.save()
                # Set last titration to now/today
                if self.titrating == False:
                    if self.ppx.prophylaxis_finished == True:
                        self.ppx.prophylaxis_finished = False
                        self.ppx.date_ended = None
                        self.ppx.save()
                    self.titrating = True
                self.last_titration = datetime.today().date()
                # Call create_labcheck() to create the next LabCheck that's due
                create_labcheck(self)
                return True
        else:
            return False

    def check_for_abnormal_labs(self, labcheck):
        """
        Method that takes a LabCheck as an argument and is called when that LabCheck is successfully updated by LabCheckUpdate view.
        Checks whether there are any abnormal labs in the LabCheck and, if so, modifies ULTPlan accordingly.
        Returns:
        boolean = True if anything was changed, False if not. Also modifies related models in the process.
        """
        def create_urgent_labcheck(self):
            """Method that creates LabCheck follow up object at urgent_lab_interval days in the future.
            Sets new LabCheck object FK to LabCheck argument in function.
            returns: nothing
            """
            LabCheck.objects.create(
                user=self.user,
                ultplan=self,
                abnormal_labcheck = labcheck,
                due=datetime.today().date() + self.urgent_lab_interval,
            )
        # Assemble dictionary of abnormal labs, None if there are none
        self.labs = labcheck.check_completed_labs()
        # If there are abnormal labs in labs (dict), set them to instance variables
        try:
            self.alt = self.labs["alt"]
        except:
            self.alt = None
        try:
            self.ast = self.labs["ast"]
        except:
            self.ast = None
        try:
            self.creatinine = self.labs["creatinine"]
        except:
            self.creatinine = None
        try:
            self.hemoglobin = self.labs["hemoglobin"]
        except:
            self.hemoglobin = None
        try:
            self.platelet = self.labs["platelet"]
        except:
            self.platelet = None
        try:
            self.wbc = self.labs["wbc"]
        except:
            self.wbc = None
        # If there are abnormal labs, process them
        if self.labs:
            # Fetch ULTPlan ULT
            self.ult = self.get_ult()
            # Fetch ULTPlan PPx
            self.ppx = self.get_ppx()
            # Fetch all LabChecks for ULTPlan
            self.labchecks = self.labcheck_set.all().order_by("-completed_date")
            # Process abnormal ALT
            if self.alt:
                if self.alt["highorlow"] == "H":
                    # If ALT is greater than 3 times the upper limit of normal
                    # Inactivate ULTPlan treatments and pause ULTPlan
                    # Create urgent LabCheck to follow up on abnormal ALT
                    if self.alt["threex"] == True:
                        self.ult.active = False
                        self.ult.save()
                        self.ppx.active = False
                        self.ppx.save()
                        self.pause = True
                        create_urgent_labcheck()
                        return True
            if self.ast:
                if self.ast["highorlow"] == "H":
                    # If AST is greater than 3 times the upper limit of normal
                    # Inactivate ULTPlan treatments and pause ULTPlan
                    # Create urgent LabCheck to follow up on abnormal AST
                    if self.ast["threex"] == True:
                        self.ult.active = False
                        self.ult.save()
                        self.ppx.active = False
                        self.ppx.save()
                        self.pause = True
                        create_urgent_labcheck()
                        return True
            if "creatinine" in self.labs:
                if self.creatinine["highorlow"] == "H":
                    # Check if there is only one completed LabCheck
                    # If so, check if User MedicalProfile has CKD == True, if not, calculate stage and mark == True
                    if len(self.labchecks) == 1:
                        # If this is the User's first LabCheck, mark CKD on MedicalProfile to True because creatinine is abnormal.
                        if self.user.medicalprofile.ckd.value == False:
                            self.user.medicalprofile.ckd.value == True
                            # Calculate CKD stage if eGFR can be calculated
                            if self.user.medicalprofile.ckd.eGFR_calculator():
                                self.user.medicalprofile.ckd.stage = self.user.medicalprofile.ckd.stage_calculator()
                            self.user.medicalprofile.ckd.save()
                        return False
                    # Check if first LabCheck creatinine was abnormal
                    elif self.labchecks[len(self.labchecks)-1].creatinine.abnormal_checker == None:
                        # If LabCheck Creatinine is < 1.5 times the upper limit of normal, schedule urgent LabCheck
                        # But continue medications, don't pause ULTPlan
                        if self.labcheck.creatinine <= self.labchecks[len(self.labchecks)-1].creatinine.var_x_high(1.5):
                            create_urgent_labcheck()
                            return True
                        # If LabCheck Creatinine is > 2.0 times the upper limit of normal, schedule urgent LabCheck.
                        # Discontinue ULT and PPx, pause ULTPlan
                        elif self.labcheck.creatinine > self.labchecks[len(self.labchecks)-1].creatinine.var_x_high(2):
                            self.ult.active = False
                            self.ult.save()
                            self.ppx.active = False
                            self.ppx.save()
                            self.pause = True
                            create_urgent_labcheck()
                            return True
                    # If first LabCheck Creatinine was abnormal, fluctuations will be larger so have more stringent criteria for follow up labs and ULTPlan modification
                    elif self.labchecks[len(self.labchecks)-1].creatinine.abnormal_checker:
                        # If LabCheck Creatinine is < 1.25 times the upper limit of normal, schedule urgent LabCheck
                        # But continue medications, don't pause ULTPlan
                        if self.labcheck.creatinine <= self.labchecks[len(self.labchecks)-1].creatinine.var_x_high(1.25):
                            create_urgent_labcheck()
                            return True
                        # If LabCheck Creatinine is > 1.5 times the upper limit of normal, schedule urgent LabCheck.
                        # Discontinue ULT and PPx, pause ULTPlan
                        elif self.labcheck.creatinine > self.labchecks[len(self.labchecks)-1].creatinine.var_x_high(1.5):
                            self.ult.active = False
                            self.ult.save()
                            self.ppx.active = False
                            self.ppx.save()
                            self.pause = True
                            create_urgent_labcheck()
                            return True
            if "hemoglobin" in self.labs:
                pass
            if "platelets" in self.labs:
                pass
            if "wbc" in self.labs:
                pass
            return False
        else:
            return False

    def __str__(self):
        return f"{str(self.user)}'s ULTPlan"

    def get_absolute_url(self):
        return reverse("ultplan:detail", kwargs={"pk": self.pk})
