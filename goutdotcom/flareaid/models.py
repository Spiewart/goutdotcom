from django.conf import settings
from django.db import models
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel

from goutdotcom.treatment.choices import BID, NAPROXEN_DOSE_CHOICES

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
from ..treatment.choices import *
from .choices import *


# Create your models here.
class FlareAid(TimeStampedModel):
    """Goal is to create a model that can make a recommendation for flare treatment."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
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
        """Class method that takes values from instance of FlareAid and returns a dictionary of the recommended treatment(s) for use in templates, other views for creating Treatment objects.
        returns {dict}: {dict} of describing treatment recommended."""
        drug1 = {
            "drug": None,
            "dose": None,
            "freq": None,
            "duration": None,
            "dose2": None,
            "freq2": None,
            "duration2": None,
            "dose3": None,
            "freq3": None,
            "duration3": None,
        }
        drug2 = {
            "drug": None,
            "dose": None,
            "freq": None,
            "duration": None,
            "dose2": None,
            "freq2": None,
            "duration2": None,
            "dose3": None,
            "freq3": None,
            "duration3": None,
        }
        decisions = {"drug1": drug1, "drug2": drug2, "needinfo": False, "doctor": False}

        if self.perfect_health == True:
            drug1["drug"] = IBUPROFEN
            drug1["dose"] = 800
            drug1["freq"] = TID
            drug1["duration"] = 7
            drug2["drug"] = NAPROXEN
            drug2["dose"] = 440
            drug2["freq"] = BID
            drug2["duration"] = 7
        elif self.perfect_health is None:
            decisions["needinfo"] = True
        if self.ckd:
            if self.ckd.value == True:
                if self.diabetes.value == True:
                    decisions["doctor"]
                else:
                    drug1["drug"] = PREDNISONE
                    drug1["dose"] = 40
                    drug1["freq"] = QDAY
                    drug1["duration"] = 4
                    drug1["dose2"] = 20
                    drug1["freq2"] = QDAY
                    drug1["duration2"] = 4
        if self.get_NSAID_contraindications():
            if self.ckd.value == True:
                drug1["drug"] = PREDNISONE
                drug1["dose"] = 40
                drug1["freq"] = QDAY
                drug1["duration"] = 4
                drug1["dose2"] = 20
                drug1["freq2"] = QDAY
            elif self.colchicine_interactions.value == True:
                drug1["drug"] = PREDNISONE
                drug1["dose"] = 40
                drug1["freq"] = QDAY
                drug1["duration"] = 4
                drug1["dose2"] = 20
                drug1["freq2"] = QDAY
                drug1["duration2"] = 4
            else:
                drug1["drug"] = COLCHICINE
                drug1["dose"] = 1.2
                drug1["freq"] = ONCE
                drug1["duration"] = 7
                drug1["dose2"] = 0.6
                drug1["freq2"] = ONCE
                drug1["dose3"] = 0.6
                drug1["freq3"] = BID
        else:
            drug1["drug"] = IBUPROFEN
            drug1["dose"] = 800
            drug1["freq"] = TID
            drug1["duration"] = 7
            drug2["drug"] = NAPROXEN
            drug2["dose"] = 440
            drug2["freq"] = BID
            drug2["duration"] = 7
        decisions["drug1"] = drug1
        decisions["drug2"] = drug2
        return decisions

    def decision_string(self, drug="drug1"):
        decisions = self.decision_aid()
        if decisions[drug]["drug"] == COLCHICINE:
            return f'{decisions[drug]["drug"]} {decisions[drug]["dose"]} mg (2 tabs) {decisions[drug]["freq"]} then {decisions[drug]["dose2"]} mg (1 tab) {decisions[drug]["freq2"]} an hour later then {decisions[drug]["dose3"]} mg {decisions[drug]["freq3"]} (twice daily) for {decisions[drug]["duration"]} days or until flare resolves'
        if decisions[drug]["drug"] == PREDNISONE:
            return f'{decisions[drug]["drug"]} {decisions[drug]["dose"]} mg {decisions[drug]["freq"]} for {decisions[drug]["duration"]} days then {decisions[drug]["dose2"]} mg {decisions[drug]["freq2"]} for {decisions[drug]["duration2"]} days'
        else:
            return f'{decisions[drug]["drug"]} {decisions[drug]["dose"]} mg {decisions[drug]["freq"]} for {decisions[drug]["duration"]} days or until flare resolves'

    def __str__(self):
        return f'{str(self.decision_aid().get("drug1"))}, {str(self.decision_aid().get("dose"))} {str(self.decision_aid().get("freq"))} {str(self.decision_aid().get("duration"))}'

    def get_absolute_url(self):
        return reverse("flareaid:detail", kwargs={"pk": self.pk})
