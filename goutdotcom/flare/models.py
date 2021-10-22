from django.conf import settings
from django.db import models
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel
from multiselectfield import MultiSelectField

from ..lab.models import Urate
from ..treatment.models import (
    Celecoxib,
    Colchicine,
    Ibuprofen,
    Meloxicam,
    Methylprednisolone,
    Naproxen,
    Othertreat,
    Prednisone,
    Tinctureoftime,
)
from .choices import *


class Flare(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    location = MultiSelectField(
        choices=JOINT_CHOICES, blank=True, null=True, help_text="What joint did the flare occur in?"
    )

    treatment = MultiSelectField(
        choices=TREATMENT_CHOICES, blank=True, null=True, help_text="What was the flare treated with?"
    )

    colchicine = models.ForeignKey(Colchicine, null=True, blank=True, on_delete=models.CASCADE)
    ibuprofen = models.ForeignKey(Ibuprofen, null=True, blank=True, on_delete=models.CASCADE)
    naproxen = models.ForeignKey(Naproxen, null=True, blank=True, on_delete=models.CASCADE)
    celecoxib = models.ForeignKey(Celecoxib, null=True, blank=True, on_delete=models.CASCADE)
    meloxicam = models.ForeignKey(Meloxicam, null=True, blank=True, on_delete=models.CASCADE)
    prednisone = models.ForeignKey(Prednisone, null=True, blank=True, on_delete=models.CASCADE)
    methylprednisolone = models.ForeignKey(Methylprednisolone, null=True, blank=True, on_delete=models.CASCADE)
    tinctureoftime = models.ForeignKey(Tinctureoftime, null=True, blank=True, on_delete=models.CASCADE)
    othertreat = models.ForeignKey(Othertreat, null=True, blank=True, on_delete=models.CASCADE)

    duration = models.IntegerField(null=True, blank=True, help_text="How long did it last? (days)")

    labs = MultiSelectField(choices=LAB_CHOICES, blank=True, null=True, help_text="Check if so")
    urate = models.OneToOneField(
        Urate,
        on_delete=models.CASCADE,
        help_text="Typically reported in mg/dL",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return f"{(str(self.user), str(self.location))}"

    def get_absolute_url(self):
        return reverse("flare:detail", kwargs={"pk": self.pk})


