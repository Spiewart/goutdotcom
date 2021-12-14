from django.conf import settings
from django.db import models
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel

from ..flare.models import Flare
from ..history.models import (
    CKD,
    IBD,
    Anticoagulation,
    Bleed,
    ColchicineInteractions,
    Diabetes,
    HeartAttack,
    Osteoporosis,
    Stroke,
)
from .choices import *


# Create your models here.
class FlareAid(TimeStampedModel):
    """Goal is to create a model that can make a recommendation for flare treatment."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
    )
    flare = models.OneToOneField(
        Flare,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
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
    anticoagulation = models.ForeignKey(
        Anticoagulation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    bleed = models.ForeignKey(
        Bleed,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    ckd = models.ForeignKey(
        CKD,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    colchicine_interactions = models.ForeignKey(
        ColchicineInteractions,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    diabetes = models.ForeignKey(
        Diabetes,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    heartattack = models.ForeignKey(
        HeartAttack,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    ibd = models.ForeignKey(
        IBD,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    osteoporosis = models.ForeignKey(
        Osteoporosis,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    stroke = models.ForeignKey(
        Stroke,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def get_NSAID_contraindications(self):
        NSAID_contraindications = []
        if self.anticoagulation:
            if self.anticoagulation.value == True:
                NSAID_contraindications.append(self.anticoagulation)
        if self.bleed:
            if self.bleed.value == True:
                NSAID_contraindications.append(self.bleed)
        if self.ckd:
            if self.ckd.value == True:
                NSAID_contraindications.append(self.ckd)
        if self.heartattack:
            if self.heartattack.value == True:
                NSAID_contraindications.append(self.heartattack)
        if self.ibd:
            if self.ibd.value == True:
                NSAID_contraindications.append(self.ibd)
        if self.stroke:
            if self.stroke.value == True:
                NSAID_contraindications.append(self.stroke)
        return NSAID_contraindications

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
        if self.ckd:
            if self.ckd.value == True:
                if self.diabetes.value == True:
                    return doctor
                else:
                    return steroids
        if self.get_NSAID_contraindications():
            if self.ckd:
                if self.ckd.value == True:
                    return steroids
            if self.colchicine_interactions:
                if self.colchicine_interactions.value == True:
                    return steroids
            else:
                return colchicine
        return NSAID

    def __str__(self):
        return self.decision_aid()

    def get_absolute_url(self):
        return reverse("flareaid:detail", kwargs={"pk": self.pk})
