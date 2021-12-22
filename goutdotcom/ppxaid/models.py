from django.conf import settings
from django.db import models
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel

from goutdotcom.treatment.choices import BID, NAPROXEN_DOSE_CHOICES

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
from ..treatment.choices import *
from ..ultaid.models import ULTAid
from .choices import *


class PPxAid(TimeStampedModel):
    """Model picking flare prophylaxis medication for use during ULT titration."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    ultaid = models.OneToOneField(
        ULTAid,
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

    def decision_aid(self):
        """Class method that takes values from instance of PPxAid and returns a dictionary of the recommended PPx treatment for use in templates, other views for creating Treatment objects.
        returns {dict}: {dict} of describing prophylactic treatment recommended."""

        decisions = {"drug": None, "dose": None, "freq": None, "needinfo": False, "doctor": False}

        if self.perfect_health == True:
            decisions["drug"] = NAPROXEN
            decisions["dose"] = 220
            decisions["freq"] = BID
        elif self.perfect_health is None:
            decisions["needinfo"] = True
        if self.ckd:
            if self.ckd.value == True:
                if self.diabetes.value == True:
                    decisions["doctor"]
                else:
                    decisions["drug"] = PREDNISONE
                    decisions["dose"] = 5
                    decisions["freq"] = QDAY
        if self.get_NSAID_contraindications():
            if self.ckd.value == True:
                decisions["drug"] = PREDNISONE
                decisions["dose"] = 5
                decisions["freq"] = QDAY
            elif self.colchicine_interactions.value == True:
                decisions["drug"] = PREDNISONE
                decisions["dose"] = 5
                decisions["freq"] = QDAY
            else:
                decisions["drug"] = COLCHICINE
                decisions["dose"] = 0.6
                decisions["freq"] = QDAY
        else:
            decisions["drug"] = NAPROXEN
            decisions["dose"] = 220
            decisions["freq"] = BID
        return decisions

    def __str__(self):
        return f'{str(self.decision_aid().get("drug"))} {str(self.decision_aid().get("dose"))} mg {str(self.decision_aid().get("freq"))}'

    def get_absolute_url(self):
        return reverse("ppxaid:detail", kwargs={"pk": self.pk})
