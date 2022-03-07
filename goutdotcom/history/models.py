from django.conf import settings
from django.db import models
from django.db.models.fields import BooleanField, IntegerField
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from multiselectfield import MultiSelectField
from simple_history.models import HistoricalRecords

from .choices import (
    BOOL_CHOICES,
    CHF_BOOL_CHOICES,
    FAMILY_CHOICES,
    LAST_MODIFIED_CHOICES,
    ORGAN_CHOICES,
)


# Create your models here.
class History(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    name = "history"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=("Do you have a " + name + "?"),
        null=True,
        blank=True,
        default=False,
    )
    last_modified = models.CharField(choices=LAST_MODIFIED_CHOICES, max_length=75, null=True, blank=True)
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("history:detail", kwargs={"pk": self.pk, "history": self.name})

    def __unicode__(self):
        return self.name


class FamilyHistory(History):
    name = "family history"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=("Do you have a family history of " + str(name) + "?"),
        null=True,
        blank=True,
        default=False,
    )
    family_member = MultiSelectField(
        choices=FAMILY_CHOICES, help_text=("Which family members had " + str(name) + "?"), default=True, null=True
    )

    class Meta:
        abstract = True


class MedicalHistory(History):
    class Meta:
        abstract = True


class MedicationHistory(History):
    class Meta:
        abstract = True

    date = models.DateField(help_text="When did you start this medication?", null=True, blank=True)


class SocialHistory(History):
    class Meta:
        abstract = True


class VascularHistory(MedicalHistory):
    class Meta:
        abstract = True

    number = models.IntegerField(help_text="How many have you had?", default=1, null=True, blank=True)
    date = models.DateField(help_text="When was it? The most recent if multiple.", null=True, blank=True)


class Alcohol(SocialHistory):
    name = "alcohol"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=("Do you drink " + name + "?"),
        verbose_name="alcohol",
        null=True,
        blank=True,
        default=False,
    )
    number = models.IntegerField(
        help_text="How many drinks do you have per week?",
        null=True,
        blank=True,
        default=False,
    )
    wine = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Do you drink wine?",
        null=True,
        blank=True,
        default=False,
    )
    beer = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Do you drink beer?",
        null=True,
        blank=True,
        default=False,
    )
    liquor = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Do you drink liquor?",
        null=True,
        blank=True,
        default=False,
    )
    name = "alcohol"


class Shellfish(SocialHistory):
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Do you eat a lot of shellfish?",
        null=True,
        blank=True,
        default=False,
        verbose_name="shellfish",
    )
    name = "shellfish"


class AllopurinolHypersensitivity(MedicalHistory):
    name = "Allopurinol Hypersensitivity"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe("Have you ever had a side effect or reaction to allopurinol?"),
        verbose_name="Allopurinol Hypersensitivity",
        null=True,
        blank=True,
        default=False,
    )
    rash = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe("Have you ever had a rash side effect due to allopurinol?."),
        verbose_name="Allopurinol Rash",
        null=True,
        blank=True,
        default=False,
    )
    transaminitis = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe("Have you ever had elevated liver function tests as a side effect of allopurinol?."),
        verbose_name="Allopurinol Transaminitis",
        null=True,
        blank=True,
        default=False,
    )
    cytopenia = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe("Have you ever had low blood counts as a side effect of allopurinol?."),
        verbose_name="Allopurinol Cytopenia",
        null=True,
        blank=True,
        default=False,
    )


class Anemia(MedicalHistory):
    """Model for history of chronic anemia. True or False."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    name = "anemia"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Do you have chronic <a href='https://www.hematology.org/education/patients/anemia' target='_blank'>anemia</a> (low hemoglobin)?"
        ),
        verbose_name="Chronic Anemia (low hemoglobin)",
        null=True,
        blank=True,
    )
    baseline = models.OneToOneField("lab.BaselineHemoglobin", on_delete=models.SET_NULL, null=True, blank=True)


class Angina(MedicalHistory):
    """Model for history of cardiac chest pain. True or False."""

    ### COULD BE EXPANDED LATER FOR UNSTABLE TO BE USED IN OTHER AIDS ###
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    name = "angina"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Do you get <a href='https://www.heart.org/en/health-topics/heart-attack/angina-chest-pain' target='_blank'>angina</a>?"
        ),
        verbose_name="Angina (cardiac chest pain)",
        null=True,
        blank=True,
    )


class Anticoagulation(MedicationHistory):
    value = BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Anticoagulation",
        help_text=mark_safe(
            "Are you on <a href='https://en.wikipedia.org/wiki/Anticoagulant' target='_blank'>anticoagulation</a> (blood thinners)</a>)?"
        ),
        null=True,
        blank=True,
        default=False,
    )
    apixaban = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Are you on apixaban / Eliquis?",
        null=True,
        blank=True,
        default=False,
    )
    clopidogrel = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Are you on clopidogrel / Plavix?",
        null=True,
        blank=True,
        default=False,
    )
    dabigatran = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Are you on dabigatran / Pradaxa?",
        null=True,
        blank=True,
        default=False,
    )
    enoxaparin = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Are you on enoxaparin / Lovenox?",
        null=True,
        blank=True,
        default=False,
    )
    rivaroxaban = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Are you on rivaroxaban / Xarelto?",
        null=True,
        blank=True,
        default=False,
    )
    warfarin = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Are you on warfarin / Coumadin?",
        null=True,
        blank=True,
        default=False,
    )
    name = "anticoagulation"


class Bleed(VascularHistory):
    name = "bleed"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Have you ever had a major bleed (<a href='https://en.wikipedia.org/wiki/Gastrointestinal_bleeding' target='_blank'>gastrointestinal bleeding</a> (GI), <a href='https://en.wikipedia.org/wiki/Peptic_ulcer_disease' target='_blank'>peptic ulcer disease</a>, brain (CNS))"
        ),
        verbose_name="major bleed",
        null=True,
        blank=True,
        default=False,
    )
    GIB = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Have you ever had <a href='https://en.wikipedia.org/wiki/Gastrointestinal_bleeding' target='_blank'>gastrointestinal bleeding</a>?"
        ),
        null=True,
        blank=True,
        default=False,
    )
    GIB_date = models.DateTimeField(
        help_text="When was the last time you has a gastrointestinal bleed?",
        default=timezone.now,
        null=True,
        blank=True,
    )
    CNS = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Have you had an intracranial bleed?",
        null=True,
        blank=True,
        default=False,
    )
    CNS_date = models.DateTimeField(
        help_text="When was the last time you had an intracranial bleed?",
        default=timezone.now,
        null=True,
        blank=True,
    )
    transfusion = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Did you require a transfusion?",
        null=True,
        blank=True,
        default=False,
    )


class CHF(MedicalHistory):
    systolic = BooleanField(
        choices=CHF_BOOL_CHOICES,
        help_text=mark_safe(
            "Do you have systolic (reduced <a href='https://en.wikipedia.org/wiki/Ejection_fraction' target='_blank'>ejection fraction</a>) heart failure?"
        ),
        verbose_name="Systolic or diastolic heart failure",
        null=True,
        blank=True,
    )
    name = "CHF"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Do you have CHF (<a href='https://en.wikipedia.org/wiki/Heart_failure' target='_blank'>congestive heart failure</a>)?"
        ),
        verbose_name="Congestive Heart Failure (CHF)",
        null=True,
        blank=True,
        default=False,
    )


class CKD(MedicalHistory):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Stage(models.IntegerChoices):
        I = 1, _("I")
        II = 2, _("II")
        III = 3, _("III")
        IV = 4, _("IV")
        V = 5, _("V")

    stage = IntegerField(
        choices=Stage.choices,
        help_text=mark_safe(
            "What <a href='https://www.kidney.org/sites/default/files/01-10-7278_HBG_CKD_Stages_Flyer_GFR.gif' target='_blank'>stage</a> is your CKD??"
        ),
        verbose_name="CKD stage",
        null=True,
        blank=False,
        default=None,
    )

    dialysis = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Are you on <a href='https://en.wikipedia.org/wiki/Hemodialysis' target='_blank'>dialysis</a>?"
        ),
        null=True,
        blank=True,
    )
    name = "CKD"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Do you have CKD (<a href='https://en.wikipedia.org/wiki/Chronic_kidney_disease' target='_blank'>chronic kidney disease</a>)?"
        ),
        verbose_name="Chronic Kidney Disease (CKD)",
        null=True,
        blank=True,
        default=False,
    )
    baseline = models.OneToOneField("lab.BaselineCreatinine", on_delete=models.SET_NULL, null=True, blank=True)


class ColchicineInteractions(MedicationHistory):
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Are you on any medications that could <a href='https://www.rxlist.com/colchicine-drug.htm#interactions' target='_blank'>interact</a> with colchicine? (common ones are simvastatin, atorvastatin, oral <a href='https://en.wikipedia.org/wiki/Antifungal' target='_blank'>antifungals</a>)?"
        ),
        verbose_name="Colchicine Medication Interactions",
        null=True,
        blank=True,
        default=False,
    )
    clarithromycin = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Are you on clarithromycin",
        null=True,
        blank=True,
        default=False,
    )
    simvastatin = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Are you on simvastatin?",
        null=True,
        blank=True,
        default=False,
    )


class Cyclosporine(MedicationHistory):
    name = "cyclosporine"


class Diabetes(MedicalHistory):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Type(models.IntegerChoices):
        One = 1
        Two = 2

    type = IntegerField(
        choices=Type.choices,
        help_text=mark_safe(
            "Do you have <a href='https://en.wikipedia.org/wiki/Type_1_diabetes' target='_blank'>type I</a> or <a href='https://en.wikipedia.org/wiki/Type_2_diabetes' target='_blank'>type II</a> diabetes?"
        ),
        verbose_name="Type 1 or type 2 diabetes?",
        null=True,
        blank=True,
    )
    insulin = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Are you on <a href='https://en.wikipedia.org/wiki/Insulin' target='_blank'>kidney stones</a>?"
        ),
        null=True,
        blank=True,
        default=False,
    )
    name = "diabetes"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Do you have <a href='https://en.wikipedia.org/wiki/Diabetes' target='_blank'>diabetes</a>?"
        ),
        verbose_name="Diabetes",
        null=True,
        blank=True,
        default=False,
    )


class Diuretics(MedicationHistory):
    hydrochlorothiazide = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Are you on hydrochlorothiazide?",
        null=True,
        blank=True,
        default=False,
    )
    furosemide = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Are you on Lasix / furosemide?",
        null=True,
        blank=True,
        default=False,
    )
    bumetanide = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Are you on Bumex / bumetanide?",
        null=True,
        blank=True,
        default=False,
    )
    torsemide = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Are you on torsemide?",
        null=True,
        blank=True,
        default=False,
    )
    metolazone = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Are you on metolazone?",
        null=True,
        blank=True,
        default=False,
    )
    name = "diuretics"


class Erosions(MedicalHistory):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = "erosions"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=("Do you have erosions on your x-rays?"),
        verbose_name="Erosions",
        null=True,
        blank=True,
        default=False,
    )


class FebuxostatHypersensitivity(MedicalHistory):
    name = "Febuxostat Hypersensitivity"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe("Have you ever had a side effect or reaction to febuxostat?"),
        verbose_name="Febuxostat Hypersensitivity",
        null=True,
        blank=True,
        default=False,
    )
    rash = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe("Have you ever had a rash side effect due to febuxostat?."),
        verbose_name="Febuxostat Rash",
        null=True,
        blank=True,
        default=False,
    )
    transaminitis = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe("Have you ever had elevated liver function tests as a side effect of febuxostat?."),
        verbose_name="Febuxostat Transaminitis",
        null=True,
        blank=True,
        default=False,
    )
    cytopenia = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe("Have you ever had low blood counts as a side effect of febuxostat?."),
        verbose_name="Febuxostat Cytopenia",
        null=True,
        blank=True,
        default=False,
    )


class Fructose(SocialHistory):
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Do you eat a lot of fructose such as the sugar found in soda/pop, processed candies, or juices?",
        null=True,
        blank=True,
        default=False,
        verbose_name="fructose",
    )
    name = "fructose"


class Gout(FamilyHistory):
    name = "gout"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Do you have a family history of gout?",
        null=True,
        blank=True,
        default=False,
    )


class HeartAttack(VascularHistory):
    name = "heart attack"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Have you ever had <a href='https://en.wikipedia.org/wiki/Myocardial_infarction' target='_blank'>heart attack</a>?"
        ),
        verbose_name="heart attack",
        null=True,
        blank=True,
        default=False,
    )
    stent = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Have you had one or more <a href='https://en.wikipedia.org/wiki/Stent' target='_blank'>stent</a> placed?"
        ),
        verbose_name="stent",
        null=True,
        blank=True,
        default=False,
    )
    stent_date = models.DateTimeField(
        help_text="When was the last time you has a stent?",
        default=timezone.now,
        null=True,
        blank=True,
    )
    cabg = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Have you had <a href='https://en.wikipedia.org/wiki/Coronary_artery_bypass_surgery' target='_blank'>bypass</a>?"
        ),
        verbose_name="cabg",
        null=True,
        blank=True,
        default=False,
    )
    cabg_date = models.DateTimeField(
        help_text="When did you have a bypass?",
        default=timezone.now,
        null=True,
        blank=True,
    )
    name = "MI"


class Hypertension(MedicalHistory):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    medication = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Are you on <a href='https://www.heart.org/en/health-topics/high-blood-pressure/changes-you-can-make-to-manage-high-blood-pressure/types-of-blood-pressure-medications' target='_blank'>medications</a> for high blood pressure?"
        ),
        verbose_name="Blood pressure medications",
        null=True,
        blank=True,
        default=False,
    )
    name = "hypertension"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Do you have <a href='https://en.wikipedia.org/wiki/Hypertension' target='_blank'>hypertension</a>?"
        ),
        verbose_name="Hypertension (high blood pressure)",
        null=True,
        blank=True,
    )


class Hyperuricemia(MedicalHistory):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = "hyperuricemia"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=("Do you have a history of elevated levels (> 9.0 mg/dL) of uric acid in your blood?"),
        verbose_name="Hyperuricemia",
        null=True,
        blank=True,
        default=False,
    )


class IBD(MedicalHistory):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = "inflammatory bowel disease"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Do you have <a href='https://en.wikipedia.org/wiki/Inflammatory_bowel_disease' target='_blank'>IBD</a> (inflammatory bowel disease=Crohn's disease or ulcerative colitis)?"
        ),
        verbose_name="Inflammatory Bowel Disease",
        null=True,
        blank=True,
        default=False,
    )


class Leukocytosis(MedicalHistory):
    """Model for history of leukocytosis. True or False."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    name = "leukocytosis"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Do you have <a href='https://www.ncbi.nlm.nih.gov/books/NBK560882/#:~:text=Leukocytosis%20is%20the%20broad%20term,identified%20by%20their%20reference%20ranges.' target='_blank'>leukocytosis</a> (elevated WBCs)?"
        ),
        verbose_name="leukocytosis (high WBCs)",
        null=True,
        blank=True,
    )
    baseline = models.OneToOneField("lab.BaselineWBC", on_delete=models.SET_NULL, null=True, blank=True)


class Leukopenia(MedicalHistory):
    """Model for history of leukopenia. True or False."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    name = "leukopenia"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Do you have <a href='https://en.wikipedia.org/wiki/Leukopenia' target='_blank'>leukopenia</a> (low WBCs)?"
        ),
        verbose_name="leukopenia (low WBCs)",
        null=True,
        blank=True,
    )
    baseline = models.OneToOneField("lab.BaselineWBC", on_delete=models.SET_NULL, null=True, blank=True)


class OrganTransplant(MedicalHistory):
    organ = MultiSelectField(
        choices=ORGAN_CHOICES,
        help_text="Which organ did you have transplanted?",
        verbose_name="Organ(s) transplanted",
        default="",
        null=True,
    )
    name = "organ transplant"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=("Have you had an " + name + "?"),
        verbose_name="Organ transplant",
        null=True,
        blank=True,
        default=False,
    )


class Osteoporosis(MedicalHistory):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = "osteoporosis"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Do you have <a href='https://en.wikipedia.org/wiki/Osteoporosis' target='_blank'>osteoporosis</a>?"
        ),
        verbose_name="Osteoporosis",
        null=True,
        blank=True,
        default=False,
    )


class Polycythemia(MedicalHistory):
    """Model for history of polycythemia. True or False."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    name = "polycythemia"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Do you have <a href='https://en.wikipedia.org/wiki/Polycythemia' target='_blank'>polycythemia</a> (high hemoglobin)?"
        ),
        verbose_name="Polycythemia (high hemoglobin)",
        null=True,
        blank=True,
    )
    baseline = models.OneToOneField("lab.BaselineHemoglobin", on_delete=models.SET_NULL, null=True, blank=True)


class PVD(MedicalHistory):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    name = "peripheral vascular disease"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Do you have <a href='https://en.wikipedia.org/wiki/Peripheral_artery_disease' target='_blank'>peripheral vascular disease</a>?"
        ),
        verbose_name="Peripheral Vascular Disease",
        null=True,
        blank=True,
    )


class Stroke(VascularHistory):
    name = "stroke"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Have you ever had <a href='https://en.wikipedia.org/wiki/Stroke' target='_blank'>stroke</a>?"
        ),
        verbose_name="stroke",
        null=True,
        blank=True,
        default=False,
    )


class Thrombocytopenia(MedicalHistory):
    """Model for history of thrombocytopenia. True or False."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    name = "thrombocytopenia"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Do you have <a href='https://www.nhlbi.nih.gov/health-topics/thrombocytopenia' target='_blank'>thrombocytopenia</a> (low platelets)?"
        ),
        verbose_name="thrombocytopenia (low platelets)",
        null=True,
        blank=True,
    )
    baseline = models.OneToOneField("lab.BaselinePlatelet", on_delete=models.SET_NULL, null=True, blank=True)


class Thrombocytosis(MedicalHistory):
    """Model for history of thrombocytosis. True or False."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    name = "thrombocytosis"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Do you have <a href='https://www.nhlbi.nih.gov/health-topics/thrombocythemia-and-thrombocytosis' target='_blank'>thrombocytosis</a> (high platelets)?"
        ),
        verbose_name="thrombocytosis (high platelets)",
        null=True,
        blank=True,
    )
    baseline = models.OneToOneField("lab.BaselinePlatelet", on_delete=models.SET_NULL, null=True, blank=True)


class Tophi(MedicalHistory):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = "tophi"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=("Do you have gouty tophi?"),
        verbose_name="Tophi",
        null=True,
        blank=True,
        default=False,
    )


class Transaminitis(MedicalHistory):
    """Model for history of transaminitis. True or False."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    name = "transaminitis"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Do you have <a href='https://en.wikipedia.org/wiki/Elevated_transaminases' target='_blank'>transaminitis</a> (elevated liver function tests)?"
        ),
        verbose_name="transaminitis (high liver function tests)",
        null=True,
        blank=True,
    )
    baseline_alt = models.OneToOneField("lab.BaselineALT", on_delete=models.SET_NULL, null=True, blank=True)
    baseline_ast = models.OneToOneField("lab.BaselineAST", on_delete=models.SET_NULL, null=True, blank=True)


class UrateKidneyStones(MedicalHistory):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = "urate kidney stones"
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Have you had urate <a href='https://en.wikipedia.org/wiki/Kidney_stone_disease' target='_blank'>kidney stones</a>?"
        ),
        verbose_name="Urate Kidney Stones",
        null=True,
        blank=True,
        default=False,
    )


class XOIInteractions(MedicationHistory):
    value = BooleanField(
        choices=BOOL_CHOICES,
        help_text=mark_safe(
            "Are you on <a href='https://en.wikipedia.org/wiki/Mercaptopurine' target='_blank'>mercaptopurine</a> (6-MP, Purixan), <a href='https://en.wikipedia.org/wiki/Azathioprine' target='_blank'>azathioprine</a> (AZA, Imuran)?"
        ),
        null=True,
        blank=True,
        default=False,
    )
    six_mp = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Are you on 6-mercaptopurine / 6-MP?",
        null=True,
        blank=True,
        default=False,
    )
    azathioprine = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Are you on azathioprine / Imuran?",
        null=True,
        blank=True,
        default=False,
    )
    name = "XOI interactions"
