from django.conf import settings
from django.db import models
from django.db.models.fields import BooleanField, IntegerField
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel
from multiselectfield import MultiSelectField

from goutdotcom.history.choices import BOOL_CHOICES, FAMILY_CHOICES, ORGAN_CHOICES


# Create your models here.
class History(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    name = "history"
    value = BooleanField(choices=BOOL_CHOICES, help_text=("Do you have " + str(name) + "?"), null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("history:detail", kwargs={"pk": self.pk, "history": self.name})

    def __unicode__(self):
        return self.name


class MedicalHistory(History):
    class Meta:
        abstract = True


class MedicationHistory(History):
    class Meta:
        abstract = True

    date = models.DateField(help_text="When did you start this medication?", null=True, blank=True)


class VascularHistory(MedicalHistory):
    class Meta:
        abstract = True

    number = models.IntegerField(help_text="How many have you had?", default=1, null=True, blank=True)
    date = models.DateField(help_text="When was it? The most recent if multiple.", null=True, blank=True)


class CKD(MedicalHistory):
    class Stage(models.IntegerChoices):
        I = 1
        II = 2
        III = 3
        IV = 4
        V = 5

    stage = IntegerField(choices=Stage.choices, help_text="What stage?", null=True, blank=True)
    dialysis = BooleanField(choices=BOOL_CHOICES, help_text="Are you on dialysis?", null=True, blank=True)
    name = "CKD"


class Hypertension(MedicalHistory):
    medication = BooleanField(
        choices=BOOL_CHOICES, help_text="Are you on medications for high blood pressure?", null=True, blank=True
    )
    name = "hypertension"


class CHF(MedicalHistory):
    systolic = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Do you have systolic (reduced ejection fraction) heart faliure?",
        null=True,
        blank=True,
    )
    name = "CHF"


class Diabetes(MedicalHistory):
    class Type(models.IntegerChoices):
        I = 1
        II = 2

    type = IntegerField(
        choices=Type.choices, help_text="Do you have type I or type II diabetes?", null=True, blank=True
    )
    insulin = BooleanField(choices=BOOL_CHOICES, help_text="Are you on insulin?", null=True, blank=True)
    name = "diabetes"


class OrganTransplant(MedicalHistory):
    organ = MultiSelectField(
        choices=ORGAN_CHOICES, help_text="Which organ did you have transplanted?", default=True, null=True
    )
    name = "organ transplant"


class UrateKidneyStones(MedicalHistory):
    name = "urate kidney stones"


class Diuretics(MedicationHistory):
    hydrochlorothiazide = BooleanField(
        choices=BOOL_CHOICES, help_text="Are you on hydrochlorothiazide?", null=True, blank=True
    )
    furosemide = BooleanField(choices=BOOL_CHOICES, help_text="Are you on Lasix / furosemide?", null=True, blank=True)
    bumetanide = BooleanField(choices=BOOL_CHOICES, help_text="Are you on Bumex / bumetanide?", null=True, blank=True)
    torsemide = BooleanField(choices=BOOL_CHOICES, help_text="Are you on torsemide?", null=True, blank=True)
    metolazone = BooleanField(choices=BOOL_CHOICES, help_text="Are you on metolazone?", null=True, blank=True)
    name = "diuretics"


class Cyclosporine(MedicationHistory):
    name = "cyclosporine"


class Anticoagulation(MedicationHistory):
    value = BooleanField(choices=BOOL_CHOICES, help_text="Are you on anticoagulation?", null=True, blank=True)
    warfarin = BooleanField(choices=BOOL_CHOICES, help_text="Are you on warfarin / Coumadin?", null=True, blank=True)
    apixaban = BooleanField(choices=BOOL_CHOICES, help_text="Are you on apixaban / Eliquis?", null=True, blank=True)
    rivaroxaban = BooleanField(
        choices=BOOL_CHOICES, help_text="Are you on rivaroxaban / Xarelto?", null=True, blank=True
    )
    clopidogrel = BooleanField(
        choices=BOOL_CHOICES, help_text="Are you on clopidogrel / Plavix?", null=True, blank=True
    )
    name = "anticoagulation"


class XOIInteractions(MedicationHistory):
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Are you on any medications that could interact with allopurinol or febuxostat? (6-mercaptopurine, azathioprine)?",
        null=True,
        blank=True,
    )
    six_mp = BooleanField(choices=BOOL_CHOICES, help_text="Are you on 6-mercaptopurine / 6-MP?", null=True, blank=True)
    azathioprine = BooleanField(
        choices=BOOL_CHOICES, help_text="Are you on azathioprine / Imuran?", null=True, blank=True
    )
    name = "allopurinol interactions"


class ColchicineInteractions(MedicationHistory):
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Are you on any medications that could interact with colchicine? (clarithromycin, simvastatin, diltiazem)",
        null=True,
        blank=True,
    )
    clarithromycin = BooleanField(choices=BOOL_CHOICES, help_text="Are you on clarithromycin", null=True, blank=True)
    simvastatin = BooleanField(choices=BOOL_CHOICES, help_text="Are you on simvastatin?", null=True, blank=True)


class Stroke(VascularHistory):
    name = "stroke"


class HeartAttack(VascularHistory):
    stent = BooleanField(choices=BOOL_CHOICES, help_text="Have you had stents placed?", null=True, blank=True)
    cabg = BooleanField(choices=BOOL_CHOICES, help_text="Have you had bypass?", null=True, blank=True)
    name = "MI"


class BleedingEvent(VascularHistory):
    GIB = BooleanField(choices=BOOL_CHOICES, help_text="Have you had a gastrointestinal bleed?", null=True, blank=True)
    CNS = BooleanField(choices=BOOL_CHOICES, help_text="Have you had an intracranial bleed?", null=True, blank=True)
    transfusion = BooleanField(choices=BOOL_CHOICES, help_text="Did you require a transfusion?", null=True, blank=True)
    name = "bleeding event"


class SocialHistory(History):
    class Meta:
        abstract = True


class Alcohol(SocialHistory):
    number = models.IntegerField(help_text="How many drinks do you have per week?", null=True, blank=True)
    wine = BooleanField(choices=BOOL_CHOICES, help_text="Do you drink wine?", null=True, blank=True)
    beer = BooleanField(choices=BOOL_CHOICES, help_text="Do you drink beer?", null=True, blank=True)
    liquor = BooleanField(choices=BOOL_CHOICES, help_text="Do you drink liquor?", null=True, blank=True)
    name = "alcohol"


class FamilyHistory(History):
    name = "family history"
    value = BooleanField(
        choices=BOOL_CHOICES, help_text=("Do you have a family history of " + str(name) + "?"), null=True, blank=True
    )
    family_member = MultiSelectField(
        choices=FAMILY_CHOICES, help_text=("Which family members had " + str(name) + "?"), default=True, null=True
    )

    class Meta:
        abstract = True


class Gout(FamilyHistory):
    name = "gout"
