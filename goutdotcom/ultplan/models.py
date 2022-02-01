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
    delinquent_lab_interval = models.DurationField(
        help_text="How long will you wait before declaring a LabCheck delinquent and pausing the ULTPlan?",
        verbose_name="Delinquent Lab Check Interval",
        default=timedelta(days=21),
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

    def create_labcheck(self, labcheck=None, shorten_by=None, urgent=False):
        """Method that creates a follow up LabCheck object.
        Checks if the urgent argument is supplied, if true sets shortens the follow up interval to urgent_lab_interval.
        Checks if ULTPLan titrating attribute is False, if so prolonged the follow up interval to monitoring_lab_interval.
        Checks if there is an associated LabCheck, sets the due date of the new LabCheck to be based off the complete_date of the FK LabCheck.
        returns: nothing
        """
        # If User's ULTPlan is no longer titrating, create LabCheck for monitoring further into the future
        if urgent == True:
            if labcheck:
                LabCheck.objects.create(
                    user=self.user,
                    ultplan=self,
                    abnormal_labcheck=labcheck,
                    due=labcheck.completed_date + self.urgent_lab_interval,
                )
            else:
                LabCheck.objects.create(
                    user=self.user,
                    ultplan=self,
                    due=datetime.today().date() + self.urgent_lab_interval,
                )
        else:
            if labcheck:
                if labcheck.completed == True:
                    if self.titrating == False:
                        LabCheck.objects.create(
                            user=self.user,
                            ultplan=self,
                            due=labcheck.completed_date + self.monitoring_lab_interval,
                        )
                    # If User's ULTPlan is still titrating (titrating == True), create LabCheck for continued titration lab monitoring
                    else:
                        if shorten_by:
                            LabCheck.objects.create(
                                user=self.user,
                                ultplan=self,
                                due=(labcheck.completed_date + self.titration_lab_interval - shorten_by),
                            )
                        else:
                            LabCheck.objects.create(
                                user=self.user,
                                ultplan=self,
                                due=(labcheck.completed_date + self.titration_lab_interval),
                            )
            else:
                if self.titrating == False:
                    LabCheck.objects.create(
                        user=self.user,
                        ultplan=self,
                        due=datetime.today().date() + self.monitoring_lab_interval,
                    )
                # If User's ULTPlan is still titrating (titrating == True), create LabCheck for continued titration lab monitoring
                else:
                    if shorten_by:
                        LabCheck.objects.create(
                            user=self.user,
                            ultplan=self,
                            due=(datetime.today().date() + self.titration_lab_interval - shorten_by),
                        )
                    else:
                        LabCheck.objects.create(
                            user=self.user,
                            ultplan=self,
                            due=(datetime.today().date() + self.titration_lab_interval),
                        )

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
            """Recursive function that takes a list of completed LabChecks, ordered by their completed_date, and a goal_urate as arguments.
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

        if labcheck.completed == True:
            # If the LabCheck is completed, fetch ULT, dose_adjustment, PPx, and all LabChecks for ULTPlan
            self.ult = self.get_ult()
            self.dose_adjustment = self.dose_adjustment
            self.ppx = self.get_ppx()
            self.labchecks = self.labcheck_set.all().order_by("-completed_date")

            if len(self.labchecks) == 1:
                # If there is only 1 LabCheck for ULTPlan, it is the first and no titration will be performed
                # Call create_labcheck() to create the next LabCheck that's due
                self.create_labcheck(labcheck=labcheck)
                return False
            if labcheck.urate.value <= self.goal_urate:
                # If LabCheck urate is less than ULTPlan goal, check if urate has been under 6.0 for 6 months or longer in order to determine whether or not to discontinue PPx
                if len(self.labchecks) > 1:
                    # If six_months_at_goal returns False, no titration performed, maintain the status quo for treatment
                    if six_months_at_goal(self.labchecks, self.goal_urate, 1) == False:
                        # Call create_labcheck() to create the next LabCheck that's due
                        self.create_labcheck(labcheck=labcheck)
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
                        self.create_labcheck(labcheck=labcheck)
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
                self.create_labcheck(labcheck=labcheck)
                return True
        else:
            return False

    def pause_treatment(self, labcheck=None):
        """Method that makes ULT and PPx inactive and pauses ULTPlan.
        Creates urgent LabCheck.
        Called when there is an urgent lab abnormality.

        Returns:
            [bool]: [bool indicating whether or not there was an abnormal lab for the LabCheck]
        """
        self.ult = self.get_ult()
        self.ult.active = False
        self.ult.save()
        self.ppx = self.get_ppx()
        self.ppx.active = False
        self.ppx.save()
        self.pause = True
        if labcheck:
            self.create_labcheck(labcheck=labcheck, urgent=True)
        else:
            self.create_labcheck(urgent=True)
        return True

    def continue_treatment(self, labcheck=None):
        """Method that creates an urgent LabCheck based off an abnormal lab.
        Takes optional LabCheck argument to associate with abnormal_labcheck.
        Does not pause ULTPlan.
        Does not make ULT and PPx inactive.

        Returns:
            [bool]: [bool indicating whether or not there was an abnormal lab for the LabCheck]
        """
        if labcheck:
            self.create_labcheck(labcheck=labcheck, urgent=True)
        else:
            self.create_labcheck(urgent=True)
        return True

    def change_therapy(self):
        """Function that checks if a ULTPLan therapy is in need of changing and does so using associated ULTAid data if so.

        returns {dict}: {dict containing drug, dose, goal uric acid, whether or not the patient is on dialysis, whether or not he or she should see a rheumatologist, and whether or not they are unwilling to take ULT.}"""

        # ult_choice dictionary is the function output for use in views, other methods, and templates
        ult_choice = {
            "drug": "allopurinol",
            "dose": 100,
            "goal_urate": 6.0,
            "titration_lab_interval": timedelta(days=42),
            "dialysis": False,
            "rheumatologist": False,
        }
        # First check if there is a medication intolerance which would prompt considering switching to the other ULT option
        if self.get_ult().intolerant == True:
            if self.get_ult()._meta.model.__name__ == "Allopurinol":
                # If there's an intolerance to the other option, rheumatologist = True for processing
                if self.user.medicalprofile.febuxostat_hypersensitivity.value == True:
                    ult_choice["rheumatologist"] = True
                # Else pick other ULT option
                else:
                    ult_choice["drug"] = "febuxostat"
                    # Dose for presence or absence of CKD
                    if self.user.medicalprofile.ckd.value == True:
                        if self.user.medicalprofile.ckd.stage != None:
                            if self.user.medicalprofile.ckd.stage < 3:
                                ult_choice["dose"] = 40
                            else:
                                ult_choice["dose"] = 20
                        else:
                            ult_choice["dose"] = 20
                    else:
                        ult_choice["dose"] = 40
            elif self.ultplan.get_ult()._meta.model.__name__ == "Febuxostat":
                # If there's an intolerance to the other option, rheumatologist = True for processing
                if self.user.medicalprofile.allopurinol_hypersensitivity.value == True:
                    ult_choice["rheumatologist"] = True
                # Dose adjust for presence/absence of CKD
                if self.user.medicalprofile.ckd.value == True:
                    if self.user.medicalprofile.ckd.stage != None:
                        if self.user.medicalprofile.ckd.stage < 3:
                            ult_choice["dose"] = 100
                    else:
                        ult_choice["dose"] = 50
        else:
            # If this isn't about a medication intolerance, then just recalculate ULTAid based on User profile options
            if (
                self.user.medicalprofile.XOI_interactions.value == True
                or self.user.medicalprofile.organ_transplant.value == True
            ):
                ult_choice["rheumatologist"] = True
            if self.user.medicalprofile.ckd.value == True:
                if self.user.medicalprofile.ckd.dialysis == True:
                    ult_choice["dialysis"] = True
                if self.user.medicalprofile.ckd.stage != None:
                    if ult_choice["drug"] == "febuxostat":
                        if self.user.medicalprofile.ckd.stage < 3:
                            ult_choice["dose"] = 40
                        else:
                            ult_choice["dose"] = 20
                    else:
                        if self.user.medicalprofile.ckd.stage < 3:
                            ult_choice["dose"] = 100
                        else:
                            ult_choice["dose"] = 50
            if self.user.medicalprofile.allopurinol_hypersensitivity.value == True:
                if (
                    self.user.medicalprofile.febuxostat_hypersensitivity.value == True
                    or self.user.medicalprofile.heartattack.value == True
                    or self.user.medicalprofile.stroke.value == True
                ):
                    ult_choice["rheumatologist"] = True
                ult_choice["drug"] = "febuxostat"
                if self.user.medicalprofile.ckd.value == True:
                    if self.user.medicalprofile.ckd.stage != None:
                        if self.user.medicalprofile.ckd.stage < 3:
                            ult_choice["dose"] = 40
                        else:
                            ult_choice["dose"] = 20
                    else:
                        ult_choice["dose"] = 20
                else:
                    ult_choice["dose"] = 40
            if self.user.medicalprofile.febuxostat_hypersensitivity.value == True:
                if self.user.medicalprofile.allopurinol_hypersensitivity.value == True:
                    ult_choice["rheumatologist"] = True
                if self.user.medicalprofile.ckd.value == True:
                    if self.user.medicalprofile.ckd.stage != None:
                        if self.user.medicalprofile.ckd.stage < 3:
                            ult_choice["dose"] = 100
                    else:
                        ult_choice["dose"] = 50
            if self.user.medicalprofile.ult.erosions.value == True or self.user.medicalprofile.ult.tophi.value == True:
                ult_choice["goal_urate"] = 5.0
        return ult_choice

    def check_for_abnormal_labs(self, labcheck):
        """
        Method that takes a LabCheck as an argument and is called when that LabCheck is successfully updated by LabCheckUpdate view.
        Checks whether there are any abnormal labs in the LabCheck and, if so, modifies ULTPlan accordingly.
        Returns:
        boolean = True if anything was changed, False if not. Also modifies related models in the process.
        """

        # Check if LabCheck is completed, which it should be based on where function is called
        if labcheck.completed == False:
            # Return None if Labcheck not completed
            return None
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
            # Bool indicating whether or not there is an urgent lab abnormality that requires calling pause_treatment()
            self.urgent_lab = False
            # Bool indicating whether or not there is a nonurgent lab abnormality that requires calling continue_treatment()
            self.nonurgent_lab = False
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
                        self.urgent_lab = True
            if self.ast:
                if self.ast["highorlow"] == "H":
                    # If AST is greater than 3 times the upper limit of normal
                    # Inactivate ULTPlan treatments and pause ULTPlan
                    # Create urgent LabCheck to follow up on abnormal AST
                    if self.ast["threex"] == True:
                        self.urgent_lab = True
            if self.creatinine:
                # Check if Creatinine abnormality is high
                if self.creatinine["highorlow"] == "H":
                    # set followup to creatinine's abnormal_high() method, sets lab urgency based on result
                    followup = labcheck.creatinine.abnormal_high(labcheck, self.labchecks)
                    if followup == "urgent":
                        self.urgent_lab = True
                    elif followup == "nonurgent":
                        self.nonurgent_lab = True
            if self.hemoglobin:
                # Check if hemoglobin is low
                if self.hemoglobin["highorlow"] == "L":
                    pass
            if self.platelet:
                # Check if platelet is high
                if self.platelet["highorlow"] == "H":
                    followup = labcheck.platelet.abnormal_high(labcheck, self.labchecks)
                    if followup == "urgent":
                        self.urgent_lab = True
                    elif followup == "nonurgent":
                        self.nonurgent_lab = True
                # Check if platelet is low
                if self.platelet["highorlow"] == "L":
                    # Check if platelet is low
                    followup = labcheck.platelet.abnormal_low(labcheck, self.labchecks)
                    if followup == "urgent":
                        self.urgent_lab = True
                    elif followup == "nonurgent":
                        self.nonurgent_lab = True
            if self.wbc:
                # Check if WBC is high
                if self.wbc["highorlow"] == "H":
                    pass
                # Check if WBC is low
                if self.wbc["highorlow"] == "L":
                    pass
            ## NEED TO CHECK OF LABCHECK IS FOLLOW UP OF ABNORMAL VALUE, WILL PROCESS DIFFERENTLY
            # If LabCheck is a follow up on an abnormal LabCheck, process differently
            if labcheck.abnormal_labcheck:
                # If urgent_lab, call pause_treatment()
                if self.urgent_lab == True:
                    return self.pause_treatment(labcheck)
                # If nonurgent_lab, create a new LabCheck when the previous titration_lab_check would have been due to continue titration()
                elif self.nonurgent_lab == True:
                    return self.create_labcheck(labcheck=labcheck, shorten_by=(self.urgent_lab_interval))
            # If urgent_lab, call pause_treatment()
            # If nonurgent_lab, call continue_treatment, which will still schedule a follow up
            else:
                if self.urgent_lab == True:
                    return self.pause_treatment(labcheck)
                elif self.nonurgent_lab == True:
                    return self.continue_treatment(labcheck)
            # Titrate if the lab abnormality is not urgent or nonurgent
            return self.titrate(labcheck)
        else:
            return self.titrate(labcheck)

    def __str__(self):
        return f"{str(self.user)}'s ULTPlan"

    def get_absolute_url(self):
        return reverse("ultplan:detail", kwargs={"pk": self.pk})
