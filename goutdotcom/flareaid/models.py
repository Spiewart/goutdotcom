from django.conf import settings
from django.db import models
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel

from .choices import *


# Create your models here.
class FlareAid(TimeStampedModel):
    """Goal is to create a model that can make a recommendation for flare treatment."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
    )

    perfect_health = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Besides having gout, are you in perfect health?",
        help_text="Meaning no chronic medical problems",
        default="",
        null=True,
        blank=True,
    )

    monoarticular = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Is your flare in just a single joint?",
        help_text="Meaning just a toe, knee, etc.",
        default="",
        null=True,
        blank=True,
    )
    ckd = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Do you have CKD?",
        help_text="Do you have CKD?",
        default="",
        null=True,
        blank=True,
    )
    diabetes = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Do you have diabetes?",
        help_text="Type I or type II",
        default="",
        null=True,
        blank=True,
    )
    NSAID_contraindication = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Have you ever had a heart attack, stroke, congestive heart failure (CHF), Crohn's disease, ulcerative colitis, or a gastrointestinal bleed? Are you on blood thinners?",
        help_text="Contraindications to NSAIDs",
        default="",
        null=True,
        blank=True,
    )
    osteoporosis = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Do you have osteoporosis?",
        help_text="Brittle bones",
        default="",
        null=True,
        blank=True,
    )
    colchicine_interactions = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Are you on simvastatin, diltiazem, or clarithromycin?",
        help_text="Contraindications to colchicine",
        default="",
        null=True,
        blank=True,
    )

    def monoarticular_aid(self):
        if self.monoarticular == True:
            return "Any monoarticular flare can be effectively treated with a corticosteroid injection by a rheumatologist or other provider."

    def decision_aid(self):
        colchicine = "colchicine"
        NSAID = "NSAID"
        steroids = "steroids"
        doctor = "doctor"
        needinfo = "Need More Information"

        if self.perfect_health == True:
            return NSAID
        elif self.perfect_health is None:
            return needinfo

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
        return reverse("flareaid:detail", kwargs={"pk": self.pk})
