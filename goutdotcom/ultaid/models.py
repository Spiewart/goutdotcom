from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_extensions.db.models import TimeStampedModel

from .choices import *

# Create your models here.
class ULTAid(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    class Stage(models.IntegerChoices):
        I = 1
        II = 2
        III = 3
        IV = 4
        V = 5

    ckd = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Do you have CKD?",
        help_text="Do you have CKD?",
        default="",
        null=True,
        blank=True,
    )
    stage = models.IntegerField(
        choices=Stage.choices,
        help_text=mark_safe(
            "What <a href='https://www.kidney.org/sites/default/files/01-10-7278_HBG_CKD_Stages_Flyer_GFR.gif' target='_blank'>stage</a> is your CKD?? If you don't know, you probably aren't."
        ),
        verbose_name="CKD stage",
        null=True,
        blank=True,
    )
    dialysis = models.BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Are you on <a href='https://en.wikipedia.org/wiki/Hemodialysis' target='_blank'>dialysis</a>? If you don't know, you probably aren't."
        ),
        null=True,
        blank=True,
    )
    XOI_interactions = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Are you on azathioprine or 6-mercaptopurine?",
        help_text="Are you on azathioprine or 6-mercaptopurine?",
        default="",
        null=True,
        blank=True,
    )
    organ_transplant = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Have you had an organ transplant?",
        help_text="Have you had an organ transplant?",
        default="",
        null=True,
        blank=True,
    )
    allopurinol_hypersensitivity = models.BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Have you ever had a <a href='https://www.nhs.uk/medicines/allopurinol/#:~:text=to%20avoid%20dehydration.-,Serious%20side%20effects,-Skin%20rashes' target='_blank'>drug-reaction to allopurinol</a>?"
        ),
        null=True,
        blank=True,
    )
    febuxostat_hypersensitivity = models.BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Have you ever had a <a href='https://www.rheumatology.org/I-Am-A/Patient-Caregiver/Treatments/Febuxostat-Uloric#:~:text=Side%20Effects,not%20be%20stopped.' target='_blank'>drug-reaction to febuxostat</a>?"
        ),
        null=True,
        blank=True,
    )
    MACE = models.BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Have you ever had <a href='https://en.wikipedia.org/wiki/Myocardial_infarction' target='_blank'>heart attack</a> or <a href='https://en.wikipedia.org/wiki/Stroke' target='_blank'>stroke</a>?"
        ),
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
        }
        if self.XOI_interactions == True or self.organ_transplant == True:
            ult_choice["rheumatologist"] = True

        if self.ckd == True:
            if self.dialysis == True:
                ult_choice["dialysis"] = True

        if self.allopurinol_hypersensitivity == True:
            if self.febuxostat_hypersensitivity == True or self.MACE == True:
                ult_choice["rheumatologist"] = True
            ult_choice["drug"] = "febuxostat"
            if self.stage >= 3:
                ult_choice["dose"] = "20 mg"
            else:
                ult_choice["dose"] = "40 mg"
            return ult_choice

        if self.febuxostat_hypersensitivity == True:
            if self.allopurinol_hypersensitivity == True:
                ult_choice["rheumatologist"] = True
            if self.stage >= 3:
                ult_choice["dose"] = "50 mg"
            return ult_choice

        return ult_choice

    def get_absolute_url(self):
        return reverse("ultaid:detail", kwargs={"pk": self.pk})
