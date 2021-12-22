from django.conf import settings
from django.db import models
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


class ULTAid(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    need = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Need ULT?",
        help_text=format_lazy("""Do you need <a href='{}' target='_blank'>ULT</a>?""", reverse_lazy("ult:create")),
    )

    want = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Want ULT?",
        help_text="Will you take daily medication to get rid of your gout?",
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
        """Function that evaluates ULTAid fields and returns a dictionary containing recommendations for ULT and other pertinent facts to the template for presentation.

        returns {dict}: {dict containing drug, dose, goal uric acid, whether or not the patient is on dialysis, whether or not he or she should see a rheumatologist, and whether or not they are unwilling to take ULT.}"""

        ### NEED TO LINK IN ULT to CALCULATE GOAL_URATE

        ult_choice = {
            "drug": "allopurinol",
            "dose": 100,
            "goal_urate": 6.0,
            "lab_interval": 42,
            "dialysis": False,
            "rheumatologist": False,
            "need": True,
            "want": True,
        }

        if self.need == True and self.want == True:
            if self.XOI_interactions.value == True or self.organ_transplant.value == True:
                ult_choice["rheumatologist"] = True

            if self.ckd.value == True:
                if self.ckd.dialysis == True:
                    ult_choice["dialysis"] = True
                if self.ckd.stage != None:
                    if ult_choice["drug"] == "febuxostat":
                        if self.ckd.stage < 3:
                            ult_choice["dose"] = 40
                        else:
                            ult_choice["dose"] = 20
                    else:
                        if self.ckd.stage < 3:
                            ult_choice["dose"] = 100
                        else:
                            ult_choice["dose"] = 50

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
                            ult_choice["dose"] = 40
                        else:
                            ult_choice["dose"] = 20
                    else:
                        ult_choice["dose"] = 20
                else:
                    ult_choice["dose"] = 40

            if self.febuxostat_hypersensitivity.value == True:
                if self.allopurinol_hypersensitivity.value == True:
                    ult_choice["rheumatologist"] = True
                if self.ckd.value == True:
                    if self.ckd.stage != None:
                        if self.ckd.stage < 3:
                            ult_choice["dose"] = 100
                    else:
                        ult_choice["dose"] = 50
            if self.user:
                if self.user.ult:
                    if self.user.ult.erosions == True or self.user.ult.tophi == True:
                        ult_choice["goal_urate"] = 5.0
        elif self.need == False and self.want == True:
            ult_choice["need"] = False
        elif self.need == True and self.want == False:
            ult_choice["want"] = False
        else:
            ult_choice["need"] = True
            ult_choice["want"] = True

        return ult_choice

    def get_absolute_url(self):
        return reverse("ultaid:detail", kwargs={"pk": self.pk})

    def __str__(self):
        if (
            self.decision_aid()["rheumatologist"] != True
            and self.decision_aid()["dialysis"] != True
            and self.decision_aid()["need"] == True
            and self.decision_aid()["want"] == True
        ):
            return f"{self.decision_aid()['drug']} {self.decision_aid()['dose']} mg daily"
        elif self.decision_aid()["rheumatologist"] == True:
            return "Rheumatologist"
        elif self.decision_aid()["dialysis"] == True:
            return "Dialysis"
        elif self.decision_aid()["need"] == False:
            return "ULT not indicated"
        elif self.decision_aid()["want"] == False:
            return "ULT not desired"
        else:
            return "Error"
