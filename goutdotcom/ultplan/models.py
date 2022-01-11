from datetime import datetime, timedelta, timezone

from django.conf import settings
from django.db import models
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel

from ..lab.models import ALT, AST, WBC, Creatinine, Hemoglobin, Platelet, Urate
from .choices import BOOL_CHOICES


class ULTPlan(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    dose_adjustment = models.IntegerField(
        help_text="What is the dose adjustment for each titration for the chosen medication?",
        verbose_name="Dose Adjustment",
        default=100,
    )
    goal_urate = models.FloatField(help_text="What is the goal uric acid?", verbose_name="Goal Uric Acid", default=6.0)
    lab_interval = models.DurationField(
        help_text="How frequently are labs required to be checked?",
        verbose_name="Lab Check Interval",
        default=timedelta(days=42),
    )
    titrating = models.BooleanField(
        choices=BOOL_CHOICES, help_text="Is this ULTPlan still in the titration phase?", default=True
    )
    last_titration = models.DateField(help_text="When was the ULT dose last titrated?", null=True, blank=True)

    def last_labcheck(self):
        """Function that fetches the last LabCheck for the ULTPlan

        Returns:
            [object]: [LabCheck]
        """
        try:
            self.labcheck = self.labcheck_set.last()
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
        """Returns ULTPlan associated ULT (allopurinol, febuxostat, probenecid)"""
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
        """Method that takes a LabCheck as an argument, checks whether or not to titrate associated ULT based off Lab values. Returns True if anything was changed, False if not. Also modifies related models in the process."""

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

        if labcheck.completed == True:
            # If the LabCheck is completed, fetch ULT, dose_adjustment, PPx, and all LabChecks for ULTPlan
            self.ult = self.get_ult()
            self.dose_adjustment = self.dose_adjustment
            self.ppx = self.get_ppx()
            self.labchecks = self.labcheck_set.all().order_by("-completed_date")

            if len(self.labchecks) == 1:
                # If there is only 1 LabCheck for ULTPlan, it is the first and no titration will be performed
                return False
            if labcheck.urate.value <= self.goal_urate:
                # If LabCheck urate is less than ULTPlan goal, check if urate has been under 6.0 for 6 months or longer in order to determine whether or not to discontinue PPx
                if len(self.labchecks) > 1:
                    # If six_months_at_goal returns False, no titration performed, maintain the status quo for treatment
                    if six_months_at_goal(self.labchecks, self.goal_urate, 1) == False:
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
                        return True
            elif labcheck.urate.value > self.goal_urate:
                # If LabCheck uric acid is higher than goal, increase ult.dose by ULTPlan dose_adjustment and save ult
                self.ult.dose = self.ult.dose + self.dose_adjustment
                self.ult.save()
                # Set last titration to now/today
                self.last_titration = datetime.today().date()
                # New LabCheck created by the view
                return True
        else:
            return False

    def __str__(self):
        return f"{str(self.user)}'s ULTPlan"

    def get_absolute_url(self):
        return reverse("ultplan:detail", kwargs={"pk": self.pk})
