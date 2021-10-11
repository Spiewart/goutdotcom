from django.conf import settings
from django.db import models
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel
from multiselectfield import MultiSelectField

from .choices import *

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

    labs = MultiSelectField(
        choices=LAB_CHOICES, blank=True, null=True, help_text="Did you get your labs checked during your flare?"
    )
    urate = models.OneToOneField(Urate, on_delete=models.CASCADE, help_text="What was the uric acid at the time of the flare?", blank=True, null=True,)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return f"{(str(self.user), str(self.location))}"

    def get_absolute_url(self):
        return reverse("flare:detail", kwargs={"pk": self.pk})


class DecisionAid(TimeStampedModel):
    """Goal is to create a model that can make a recommendation for flare treatment."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
    )

    perfect_health = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Are you in perfect health?",
        help_text="Meaning no chronic medical problems",
        default=False,
        null=True,
        blank=True,
    )

    monoarticular = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Is your flare in just a single joint?",
        help_text="Meaning just a toe, knee, etc.",
        default=False,
        null=True,
        blank=True,
    )
    ckd = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Do you have CKD?",
        help_text="Do you have CKD?",
        default=False,
        null=True,
        blank=True,
    )
    diabetes = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Do you have diabetes?",
        help_text="Type I or type II",
        default=False,
        null=True,
        blank=True,
    )
    NSAID_contraindication = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Have you ever had a heart attack, stroke, congestive heart failure (CHF), Crohn's disease, ulcerative colitis, or a gastrointestinal bleed? Are you on blood thinners?",
        help_text="Contraindications to NSAIDs",
        default=False,
        null=True,
        blank=True,
    )
    osteoporosis = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Do you have osteoporosis?",
        help_text="Brittle bones",
        default=False,
        null=True,
        blank=True,
    )
    colchicine_contraindication = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Are you on simvastatin, diltiazem, or clarithromycin?",
        help_text="Contraindications to colchicine",
        default=False,
        null=True,
        blank=True,
    )

    def decision_aid(self):
        colchicine = "colchicine"
        injection = "injection"
        NSAID = "NSAID"
        steroids = "steroids"
        doctor = "doctor"

        if self.perfect_health == True:
            return NSAID

        if self.ckd == True:
            if self.diabetes == True:
                return doctor
            else:
                return steroids

        if self.NSAID_contraindication == True:
            if self.ckd == True:
                return steroids
            if self.colchicine_contraindication == True:
                return steroids
            else:
                return colchicine

        return NSAID

    def __str__(self):
        return self.decision_aid()

    def get_absolute_url(self):
        return reverse("flare:decisionaid-detail", kwargs={"pk": self.pk})
