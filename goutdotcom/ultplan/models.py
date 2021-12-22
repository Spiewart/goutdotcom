from datetime import datetime

from django.conf import settings
from django.db import models
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel

from ..ppxaid.models import PPxAid
from ..ultaid.models import ULTAid
from .choices import BOOL_CHOICES

class ULTPlan(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ultaid = models.OneToOneField(ULTAid, on_delete=models.CASCADE)
    ppxaid = models.OneToOneField(PPxAid, on_delete=models.CASCADE)

    goal_urate = models.FloatField(help_text="What is the goal uric acid?", verbose_name="Goal Uric Acid", default=6.0)
    lab_interval = models.IntegerField(
        help_text="How frequently are labs required to be checked?", verbose_name="Lab Check Interval", default=42
    )
    titrating = models.BooleanField(
        choices=BOOL_CHOICES, help_text="Is this ULTPlan still in the titration phase?", default=True
    )
    last_titration = models.DateField(help_text="When was the ULT dose last titrated?", null=True, blank=True)

    def ALT_status(self):
        try:
            self.alt = self.ALT.last()
        except:
            self.alt = None
        if self.alt:
            if datetime.today() - self.alt.created >= 60:
                due = True
            else:
                due = False
        else:
            due = True
        return due

    def AST_status(self):
        try:
            self.ast = self.AST.last()
        except:
            self.ast = None
        if self.ast:
            if datetime.today() - self.ast.created >= 60:
                due = True
            else:
                due = False
        else:
            due = True
        return due

    def creatinine_status(self):
        try:
            self.creatinine = self.Creatinine.last()
        except:
            self.creatinine = None
        if self.creatinine:
            if datetime.today() - self.creatinine.created >= 60:
                due = True
            else:
                due = False
        else:
            due = True
        return due

    def hemoglobin_status(self):
        try:
            self.hemoglobin = self.Hemoglobin.last()
        except:
            self.hemoglobin = None
        if self.hemoglobin:
            if datetime.today() - self.hemoglobin.created >= 60:
                due = True
            else:
                due = False
        else:
            due = True
        return due

    def platelet_status(self):
        try:
            self.platelet = self.Platelet.last()
        except:
            self.platelet = None
        if self.platelet:
            if datetime.today() - self.platelet.created >= 60:
                due = True
            else:
                due = False
        else:
            due = True
        return due

    def WBC_status(self):
        try:
            self.wbc = self.WBC.last()
        except:
            self.wbc = None
        if self.wbc:
            if datetime.today() - self.wbc.created >= 60:
                due = True
            else:
                due = False
        else:
            due = True
        return due

    def urate_status(self):
        try:
            self.urate = self.Urate.last()
        except:
            self.urate = None
        if self.urate:
            if datetime.today() - self.urate.created >= 60:
                due = True
            else:
                due = False
        else:
            due = True
        return due

    def lab_status(self):
        if (
            self.AST_status() == False
            and self.ALT_status() == False
            and self.creatinine_status() == False
            and self.hemoglobin_status() == False
            and self.platelet_status() == False
            and self.WBC_status() == False
            and self.urate_status() == False
        ):
            return True
        else:
            overdue_labs = []
            if self.AST_status() == True:
                overdue_labs.append("AST")
            if self.ALT_status() == True:
                overdue_labs.append("ALT")
            if self.creatinine_status() == True:
                overdue_labs.append("creatinine")
            if self.hemoglobin_status() == True:
                overdue_labs.append("hemoglobin")
            if self.platelet_status() == True:
                overdue_labs.append("platelets")
            if self.WBC_status() == True:
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

    def __str__(self):
        return f"{str(self.user)}'s ULTPlan"

    def get_absolute_url(self):
        return reverse("ultplan:detail", kwargs={"pk": self.pk})
