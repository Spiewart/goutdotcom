from datetime import datetime

from django.conf import settings
from django.db import models
from django.db.models.expressions import Col
from django.db.models.fields import BooleanField
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.text import format_lazy
from django_extensions.db.models import TimeStampedModel

from ..lab.models import ALT, AST, WBC, Creatinine, Hemoglobin, Platelet, Urate
from ..ppxaid.models import PPxAid
from ..treatment.models import (
    Allopurinol,
    Colchicine,
    Febuxostat,
    Ibuprofen,
    Naproxen,
    Prednisone,
    Probenecid,
)
from ..ultaid.models import ULTAid
from .choices import BOOL_CHOICES


class ULTPlan(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ultaid = models.OneToOneField(ULTAid, on_delete=models.CASCADE)
    ppxaid = models.OnetoOneField(PPxAid, on_delete=models.CASCADE)
    allopurinol = models.OneToOneField(Allopurinol, on_delete=models.CASCADE, null=True, blank=True, default=None)
    febuxostat = models.OneToOneField(Febuxostat, on_delete=models.CASCADE, null=True, blank=True, default=None)
    probenecid = models.OneToOneField(Probenecid, on_delete=models.CASCADE, null=True, blank=True, default=None)
    ibuprofen = models.OneToOneField(Ibuprofen, on_delete=models.CASCADE, null=True, blank=True, default=None)
    naproxen = models.OneToOneField(Naproxen, on_delete=models.CASCADE, null=True, blank=True, default=None)
    colchicine = models.OneToOneField(Colchicine, on_delete=models.CASCADE, null=True, blank=True, default=None)
    prednisone = models.OneToOneField(Prednisone, on_delete=models.CASCADE, null=True, blank=True, default=None)

    goal_urate = models.FloatField(help_text="What is the goal uric acid?", verbose_name="Goal Uric Acid", default=6.0)
    lab_interval = models.IntegerField(
        help_text="How frequently are labs required to be checked?", verbose_name="Lab Check Interval", default=42
    )
    titrating = models.BooleanField(
        choices=BOOL_CHOICES, help_text="Is this ULTPlan still in the titration phase?", default=True
    )
    last_titration = models.DateField(help_text="When was the ULT dose last titrated?", null=True, blank=True)

    def AST_status(self):
        ast = AST.objects.filter(user=self.user, ultplan__pk=self.pk).last()
        due = False
        if datetime.today() - ast.created >= 60:
            due = True
        return due

    def ALT_status(self):
        alt = ALT.objects.filter(user=self.user, ultplan__pk=self.pk).last()
        due = False
        if datetime.today() - alt.created >= 60:
            due = True
        return due

    def creatinine_status(self):
        creatinine = Creatinine.objects.filter(user=self.user, ultplan__pk=self.pk).last()
        due = False
        if datetime.today() - creatinine.created >= 60:
            due = True
        return due

    def hemoglobin_status(self):
        hemoglobin = Hemoglobin.objects.filter(user=self.user, ultplan__pk=self.pk).last()
        due = False
        if datetime.today() - hemoglobin.created >= 60:
            due = True
        return due

    def platelet_status(self):
        platelet = Platelet.objects.filter(user=self.user, ultplan__pk=self.pk).last()
        due = False
        if datetime.today() - platelet.created >= 60:
            due = True
        return due

    def WBC_status(self):
        wbc = WBC.objects.filter(user=self.user, ultplan__pk=self.pk).last()
        due = False
        if datetime.today() - wbc.created >= 60:
            due = True
        return due

    def urate_status(self):
        urate = Urate.objects.filter(user=self.user, ultplan__pk=self.pk).last()
        due = False
        if datetime.today() - urate.created >= 60:
            due = True
        return due

    def lab_status(self):
        if self.AST_status() == False and self.ALT_status() == False and self.creatinine_status() == False and self.hemoglobin_status() == False and self.platelet_status() == False and self.WBC_status() == False and self.urate_status() == False:
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
                for i in range(len(overdue_labs)-1):
                    overdue_labs_string += overdue_labs[i]
                    overdue_labs_string += ", "
                overdue_labs_string += overdue_labs[len(overdue_labs)-1]
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
