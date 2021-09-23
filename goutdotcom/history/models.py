from django.conf import settings
from django.db import models
from django.db.models.fields import BooleanField, IntegerField
from django.urls import reverse
from django.utils import timezone
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
    value = BooleanField(choices=BOOL_CHOICES, help_text=("Do you have a " + name + "?"), null=True, blank=True)

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

    stage = IntegerField(
        choices=Stage.choices,
        help_text="What stage is your CKD? If you don't know, skip this or leave it blank.",
        verbose_name="CKD stage",
        null=True,
        blank=True,
    )
    dialysis = BooleanField(choices=BOOL_CHOICES, help_text="Are you on dialysis?", null=True, blank=True)
    name = "CKD"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=("Do you have " + name + "?"),
        verbose_name="Chronic kidney disease (CKD)",
        null=True,
        blank=True,
    )


class Hypertension(MedicalHistory):
    medication = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Are you on medications for high blood pressure?",
        verbose_name="Blood pressure medications",
        null=True,
        blank=True,
    )
    name = "hypertension"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=("Do you have " + name + "?"),
        verbose_name="Hypertension (high blood pressure)",
        null=True,
        blank=True,
    )


class CHF(MedicalHistory):
    systolic = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Do you have systolic (reduced ejection fraction) heart faliure? If you don't know, skip this or leave it blank.",
        verbose_name="Systolic or diastolic heart failure",
        null=True,
        blank=True,
    )
    name = "CHF"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=("Do you have " + name + "?"),
        verbose_name="Congestive heart failure (CHF)",
        null=True,
        blank=True,
    )


class Diabetes(MedicalHistory):
    class Type(models.IntegerChoices):
        I = 1
        II = 2

    type = IntegerField(
        choices=Type.choices,
        help_text="Do you have type I or type II diabetes?",
        verbose_name="Type 1 or type 2 diabetes?",
        null=True,
        blank=True,
    )
    insulin = BooleanField(choices=BOOL_CHOICES, help_text="Are you on insulin?", null=True, blank=True)
    name = "diabetes"
    value = BooleanField(
        choices=BOOL_CHOICES, help_text=("Do you have " + name + "?"), verbose_name="Diabetes", null=True, blank=True
    )


class OrganTransplant(MedicalHistory):
    organ = MultiSelectField(
        choices=ORGAN_CHOICES,
        help_text="Which organ did you have transplanted?",
        verbose_name="Organ(s) transplanted",
        default=True,
        null=True,
    )
    name = "organ transplant"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=("Do you have " + name + "?"),
        verbose_name="Organ transplant",
        null=True,
        blank=True,
    )


class UrateKidneyStones(MedicalHistory):
    name = "urate kidney stones"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=("Do you have a history of " + name + "?"),
        verbose_name="Urate Kidney Stones",
        null=True,
        blank=True,
    )


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
    apixaban = BooleanField(choices=BOOL_CHOICES, help_text="Are you on apixaban / Eliquis?", null=True, blank=True)

    clopidogrel = BooleanField(
        choices=BOOL_CHOICES, help_text="Are you on clopidogrel / Plavix?", null=True, blank=True
    )
    dabigatran = BooleanField(choices=BOOL_CHOICES, help_text="Are you on dabigatran / Pradaxa?", null=True, blank=True)
    enoxaparin = BooleanField(choices=BOOL_CHOICES, help_text="Are you on enoxaparin / Lovenox?", null=True, blank=True)
    rivaroxaban = BooleanField(
        choices=BOOL_CHOICES, help_text="Are you on rivaroxaban / Xarelto?", null=True, blank=True
    )
    warfarin = BooleanField(choices=BOOL_CHOICES, help_text="Are you on warfarin / Coumadin?", null=True, blank=True)
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
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=("Have you ever had a " + name + "?"),
        verbose_name="stroke",
        null=True,
        blank=True,
    )


class HeartAttack(VascularHistory):
    name = "heart attack"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=("Have you ever had a " + name + "?"),
        verbose_name="heart attack",
        null=True,
        blank=True,
    )
    stent = BooleanField(
        choices=BOOL_CHOICES, help_text="Have you had stents placed?", verbose_name="stent", null=True, blank=True
    )
    stent_date = models.DateTimeField(
        help_text="When was the last time you has a stent?",
        default=timezone.now,
        null=True,
        blank=True,
    )
    cabg = BooleanField(
        choices=BOOL_CHOICES, help_text="Have you had bypass?", verbose_name="cabg", null=True, blank=True
    )
    cabg_date = models.DateTimeField(
        help_text="When did you have a bypass?",
        default=timezone.now,
        null=True,
        blank=True,
    )
    name = "MI"


class Bleed(VascularHistory):
    name = "bleed"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=("Have you ever had a " + name + "?"),
        verbose_name="major bleed",
        null=True,
        blank=True,
    )
    GIB = BooleanField(choices=BOOL_CHOICES, help_text="Have you had a gastrointestinal bleed?", null=True, blank=True)
    GIB_date = models.DateTimeField(
        help_text="When was the last time you has a gastrointestinal bleed?",
        default=timezone.now,
        null=True,
        blank=True,
    )
    CNS = BooleanField(choices=BOOL_CHOICES, help_text="Have you had an intracranial bleed?", null=True, blank=True)
    CNS_date = models.DateTimeField(
        help_text="When was the last time you had an intracranial bleed?", default=timezone.now, null=True, blank=True
    )
    transfusion = BooleanField(choices=BOOL_CHOICES, help_text="Did you require a transfusion?", null=True, blank=True)


class SocialHistory(History):
    class Meta:
        abstract = True


class Alcohol(SocialHistory):
    name = "alcohol"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=("Do you drink " + name + "?"),
        verbose_name="alcohol",
        null=True,
        blank=True,
    )
    number = models.IntegerField(help_text="How many drinks do you have per week?", null=True, blank=True)
    wine = BooleanField(choices=BOOL_CHOICES, help_text="Do you drink wine?", null=True, blank=True)
    beer = BooleanField(choices=BOOL_CHOICES, help_text="Do you drink beer?", null=True, blank=True)
    liquor = BooleanField(choices=BOOL_CHOICES, help_text="Do you drink liquor?", null=True, blank=True)
    name = "alcohol"


class Fructose(SocialHistory):
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Do you eat a lot of fructose such as the sugar found in soda/pop, processed candies, or juices?",
        null=True,
        blank=True,
        verbose_name="fructose",
    )
    name = "fructose"


class Shellfish(SocialHistory):
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Do you eat a lot of shellfish?",
        null=True,
        blank=True,
        verbose_name="shellfish",
    )
    name = "shellfish"


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
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Do you have a family history of gout?",
        null=True,
        blank=True,
    )
