from datetime import datetime, timedelta, timezone

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

    def lab_status(self, lab):
        lab_set = f"{lab}_set"
        try:
            self.lab = self.lab_set.last()
        except:
            self.lab = None
        if self.lab:
            if datetime.now(timezone.utc) - self.lab.created >= timedelta(days=self.lab_interval):
                due = True
            else:
                due = False
        else:
            due = True
        return due

    def labs_due(self):
        if (
            self.lab_status("alt") == False
            and self.lab_status("ast") == False
            and self.lab_status("creatinine") == False
            and self.lab_status("hemoglobin") == False
            and self.lab_status("platelet") == False
            and self.lab_status("wbc") == False
            and self.lab_status("urate") == False
        ):
            return True
        else:
            overdue_labs = []
            if self.lab_status("alt")  == True:
                overdue_labs.append("ALT")
            if self.lab_status("ast") == True:
                overdue_labs.append("AST")
            if self.lab_status("creatinine") == True:
                overdue_labs.append("creatinine")
            if self.lab_status("hemoglobin") == True:
                overdue_labs.append("hemoglobin")
            if self.lab_status("platelet") == True:
                overdue_labs.append("platelets")
            if self.lab_status("wbc") == True:
                overdue_labs.append("WBC")
            if self.lab_status("urate") == True:
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
