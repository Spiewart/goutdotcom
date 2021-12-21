from django.conf import settings
from datetime import datetime
from django.db import models
from django.db.models.expressions import Col
from django.db.models.fields import BooleanField
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.text import format_lazy
from django_extensions.db.models import TimeStampedModel

from ..lab.models import (
    AST,
    ALT,
    Creatinine,
    Hemoglobin,
    WBC,
    Platelet,
    Urate,
)
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
    allopurinol = models.OneToOneField(Allopurinol, on_delete=models.CASCADE, null=True, blank=True)
    febuxostat = models.OneToOneField(Febuxostat, on_delete=models.CASCADE, null=True, blank=True)
    probenecid = models.OneToOneField(Probenecid, on_delete=models.CASCADE, null=True, blank=True)
    ibuprofen = models.OneToOneField(Ibuprofen, on_delete=models.CASCADE, null=True, blank=True)
    naproxen = models.OneToOneField(Naproxen, on_delete=models.CASCADE, null=True, blank=True)
    colchicine = models.OneToOneField(Colchicine, on_delete=models.CASCADE, null=True, blank=True)
    prednisone = models.OneToOneField(Prednisone, on_delete=models.CASCADE, null=True, blank=True)

    goal_urate = models.FloatField(help_text="What is the goal uric acid?", verbose_name="Goal Uric Acid", default=6.0)
    lab_interval = models.IntegerField(
        help_text="How frequently are labs required to be checked?", verbose_name="Lab Check Interval", default=42
    )
    titrating = models.BooleanField(
        choices=BOOL_CHOICES, help_text="Is this ULTPlan still in the titration phase?", default=True
    )

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

    def __str__(self):
        return f"{str(self.user)}'s ULTPlan"

    def get_absolute_url(self):
        return reverse("ultplan:detail", kwargs={"pk": self.pk})
