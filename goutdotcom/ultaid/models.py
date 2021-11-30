from django.conf import settings
from django.db import models
from django.db.models.fields import BooleanField
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.text import format_lazy
from django_extensions.db.models import TimeStampedModel

from goutdotcom.history.models import HeartAttack

from ..history.models import (
    CKD,
    AllopurinolHypersensitivity,
    FebuxostatHypersensitivity,
    HeartAttack,
    OrganTransplant,
    Stroke,
    XOIInteractions,
)
from .choices import *


# Create your models here.
class ULTAid(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    need = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Need ULT?",
        help_text=format_lazy("""Do you need <a href='{}' target='_blank'>ULT</a>?""", reverse_lazy("ult:create")),
        default="",
        null=True,
        blank=True,
    )

    want = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Want ULT?",
        help_text="Will you take daily medication to get rid of your gout?",
        default="",
        null=True,
        blank=True,
    )

    ckd = models.ForeignKey(
        CKD,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    XOI_interactions = models.ForeignKey(
        XOIInteractions,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    organ_transplant = models.ForeignKey(
        OrganTransplant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    allopurinol_hypersensitivity = models.ForeignKey(
        AllopurinolHypersensitivity,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=mark_safe(
            "Have you ever had a <a href='https://www.nhs.uk/medicines/allopurinol/#:~:text=to%20avoid%20dehydration.-,Serious%20side%20effects,-Skin%20rashes' target='_blank'>drug-reaction to allopurinol</a>?"
        ),
    )

    febuxostat_hypersensitivity = models.ForeignKey(
        FebuxostatHypersensitivity,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=mark_safe(
            "Have you ever had a <a href='https://www.rheumatology.org/I-Am-A/Patient-Caregiver/Treatments/Febuxostat-Uloric#:~:text=Side%20Effects,not%20be%20stopped.' target='_blank'>drug-reaction to febuxostat</a>?"
        ),
    )
    heartattack = models.ForeignKey(
        HeartAttack,
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

    def decision_aid(self):
        ult_choice = {
            "drug": "allopurinol",
            "dose": "100 mg",
            "goal_urate": "6.0 mg/dL",
            "dialysis": False,
            "rheumatologist": False,
            "unwilling": False,
        }
        if self.XOI_interactions.value == True or self.organ_transplant.value == True:
            ult_choice["rheumatologist"] = True

        if self.ckd.value == True:
            if self.ckd.dialysis == True:
                ult_choice["dialysis"] = True
            if self.ckd.stage != None:
                if ult_choice["drug"] == "febuxostat":
                    if self.ckd.stage < 3:
                        ult_choice["dose"] = "40 mg"
                    else:
                        ult_choice["dose"] = "20 mg"
                else:
                    if self.ckd.stage < 3:
                        ult_choice["dose"] = "100 mg"
                    else:
                        ult_choice["dose"] = "50 mg"

        if self.allopurinol_hypersensitivity.value == True:
            if (
                self.febuxostat_hypersensitivity.value == True
                or self.heartattack.value == True
                or self.stroke.value == True
            ):
                ult_choice["rheumatologist"] = True
            ult_choice["drug"] = "febuxostat"
            if self.ckd.value == True:
                if self.ckd.stage != None:
                    if self.ckd.stage < 3:
                        ult_choice["dose"] = "40 mg"
                    else:
                        ult_choice["dose"] = "20 mg"
                else:
                    ult_choice["dose"] = "20 mg"
            else:
                ult_choice["dose"] = "40 mg"
            return ult_choice

        if self.febuxostat_hypersensitivity.value == True:
            if self.allopurinol_hypersensitivity.value == True:
                ult_choice["rheumatologist"] = True
            if self.ckd.value == True:
                if self.ckd.stage != None:
                    if self.ckd.stage < 3:
                        ult_choice["dose"] = "100 mg"
                else:
                    ult_choice["dose"] = "50 mg"
            return ult_choice

        return ult_choice

    def get_absolute_url(self):
        return reverse("ultaid:detail", kwargs={"pk": self.pk})
