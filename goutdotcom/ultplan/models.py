from datetime import datetime, timedelta, timezone

from django.conf import settings
from django.db import models
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel

from ..lab.models import LabCheck
from .choices import BOOL_CHOICES


class ULTPlan(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    dose_adjustment = models.IntegerField(
        help_text="What is the dose adjustment for each titration for the chosen medication?",
        verbose_name="Dose Adjustment",
        default=100,
    )
    goal_urate = models.FloatField(help_text="What is the goal uric acid?", verbose_name="Goal Uric Acid", default=6.0)
    lab_interval = models.IntegerField(
        help_text="How frequently are labs required to be checked?", verbose_name="Lab Check Interval", default=42
    )
    titrating = models.BooleanField(
        choices=BOOL_CHOICES, help_text="Is this ULTPlan still in the titration phase?", default=True
    )
    last_titration = models.DateField(help_text="When was the ULT dose last titrated?", null=True, blank=True)

    def alt_status(self):
        # Takes
        try:
            self.alt = self.alt_set.last()
        except:
            self.alt = None
        if self.alt:
            if datetime.now(timezone.utc) - self.alt.created >= timedelta(days=self.lab_interval):
                due = True
            else:
                due = False
        else:
            due = True
        return due

    def ast_status(self):
        # Takes
        try:
            self.ast = self.ast_set.last()
        except:
            self.ast = None
        if self.ast:
            if datetime.now(timezone.utc) - self.ast.created >= timedelta(days=self.lab_interval):
                due = True
            else:
                due = False
        else:
            due = True
        return due

    def creatinine_status(self):
        # Takes
        try:
            self.creatinine = self.creatinine_set.last()
        except:
            self.creatinine = None
        if self.creatinine:
            if datetime.now(timezone.utc) - self.creatinine.created >= timedelta(days=self.lab_interval):
                due = True
            else:
                due = False
        else:
            due = True
        return due

    def hemoglobin_status(self):
        # Takes
        try:
            self.hemoglobin = self.hemoglobin_set.last()
        except:
            self.hemoglobin = None
        if self.hemoglobin:
            if datetime.now(timezone.utc) - self.hemoglobin.created >= timedelta(days=self.lab_interval):
                due = True
            else:
                due = False
        else:
            due = True
        return due

    def platelet_status(self):
        # Takes
        try:
            self.platelet = self.platelet_set.last()
        except:
            self.platelet = None
        if self.platelet:
            if datetime.now(timezone.utc) - self.platelet.created >= timedelta(days=self.lab_interval):
                due = True
            else:
                due = False
        else:
            due = True
        return due

    def wbc_status(self):
        # Takes
        try:
            self.wbc = self.wbc_set.last()
        except:
            self.wbc = None
        if self.ast:
            if datetime.now(timezone.utc) - self.wbc.created >= timedelta(days=self.lab_interval):
                due = True
            else:
                due = False
        else:
            due = True
        return due

    def urate_status(self):
        """Model method that determines if the ULTPlan has an associated uric acid within the defined lab interval (preceding x number of days)"""
        try:
            self.urate = self.urate_set.last()
        except:
            self.urate = None
        if self.urate:
            if datetime.now(timezone.utc) - self.urate.created >= timedelta(days=self.lab_interval):
                due = True
            else:
                due = False
        else:
            due = True
        return due

    def labs_due(self):
        if (
            self.alt_status() == False
            and self.ast_status() == False
            and self.creatinine_status() == False
            and self.hemoglobin_status() == False
            and self.platelet_status() == False
            and self.wbc_status() == False
            and self.urate_status() == False
        ):
            return True
        else:
            overdue_labs = []
            if self.alt_status() == True:
                overdue_labs.append("ALT")
            if self.ast_status() == True:
                overdue_labs.append("AST")
            if self.creatinine_status() == True:
                overdue_labs.append("creatinine")
            if self.hemoglobin_status() == True:
                overdue_labs.append("hemoglobin")
            if self.platelet_status() == True:
                overdue_labs.append("platelets")
            if self.wbc_status() == True:
                overdue_labs.append("WBC")
            if self.urate_status() == True:
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

    def titration_due(self):
        if datetime.today() - self.last_titration > self.lab_interval:
            return True
        else:
            return False

    def titrate(self):
        if self.titration_due() == True:
            pass
        elif self.titration_due() == False:
            pass
        else:
            pass

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

    def __str__(self):
        return f"{str(self.user)}'s ULTPlan"

    def get_absolute_url(self):
        return reverse("ultplan:detail", kwargs={"pk": self.pk})


class Titration(TimeStampedModel):
    """Model to generate a titration object. Related fields"""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ultplan = models.ForeignKey(ULTPlan, on_delete=models.CASCADE)
    labcheck = models.OneToOneField(LabCheck, on_delete=models.CASCADE)

    def titrate(self):
        if self.labcheck.completed == True:
            self.ult = self.ultplan.get_ult()
            self.dose_adjustment = self.ultplan.dose_adjustment
            self.ppx = self.ultplan.get_ppx()
            try:
                self.urates = self.ultplan.urate_set
            except:
                self.urates = None
            if self.labcheck.urate.value <= self.ultplan.goal_urate:

                self.urates = self.urates.objects.filter(
                    user=self.user,
                    ultplan=self.ultplan,
                    created__range=[
                        datetime.now(timezone.utc) - timedelta(days=365),
                        datetime.now(timezone.utc),
                    ],
                )
                self.last_six_urates = self.urates.filter(
                    created__range=[
                        datetime.now(timezone.utc) - timedelta(days=180),
                        datetime.now(timezone.utc),
                    ],
                )
                if len(self.urates) == 1:
                    pass
                if len(self.urates) > 1:
                    if len(self.last_six_urates) > 1:
                        for urate in self.last_six_urates:
                            if urate.value < 6:
                                pass

                    for urate in self.urates:
                        if urate.value < 6:
                            pass
                else:
                    pass
            if self.urate.value > self.ultplan.goal_urate:
                self.ult.dose = self.ult.dose + self.dose_adjustment
                self.ult.dose.save()
                LabCheck.objects.create(user=self.user, ultplan=self.ultplan)
