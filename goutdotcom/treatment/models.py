import datetime
from decimal import *

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel

from .choices import *


# Create your models here.
class Treatment(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES)
    brand_names = [""]
    dose = models.IntegerField(null=True, blank=True)
    freq = models.CharField(max_length=50, choices=FREQ_CHOICES, default=QDAY, null=True, blank=True)
    side_effects = models.CharField(max_length=100, null=True, blank=True, help_text="Have you had any side effects?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES)

    class Meta:
        abstract = True

    def __str__(self):
        if self.dose:
            return f'{str(self.generic_name) + " " + str(self.dose) + " mg " + str(self.freq)}'
        else:
            return f'{str(self.generic_name) + " (dose not recorded)"}'

    def get_absolute_url(self):
        return reverse("treatment:detail", kwargs={"pk": self.pk, "treatment": self.generic_name})

    def __unicode__(self):
        return self.generic_name


class FlareAidTreatment(Treatment):
    prn = models.BooleanField(
        choices=BOOL_CHOICES,
        default=True,
        null=True,
        blank=True,
        help_text="Do you take this medication only as needed (PRN)?",
    )
    as_prophylaxis = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Flare prophylaxis?",
        help_text="Is this for flare prophylaxis while initiating ULT?",
        default=False,
        blank=True,
        null=True,
    )

    duration = models.IntegerField(
        null=True, blank=True, default=7, validators=[MaxValueValidator(14), MinValueValidator(1)]
    )

    def flareclaimer(self):
        natural_history = "Most flares last between 5-7 days. Flare treatments are design to improve (not eliminate) symptoms over that duration. If your symptoms improve more quickly, it is OK to discontinue your flare treatment early. If your symptoms last longer, you should consult your provider."
        return natural_history

    class Meta:
        abstract = True


class ULTAidTreatment(Treatment):
    date_started = models.DateField(default=datetime.datetime.now, null=True, blank=True)
    date_ended = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True


class Allopurinol(ULTAidTreatment):
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=ALLOPURINOL)
    brand_names = ["Xyloprim", "Aloprim"]
    dose = models.IntegerField(choices=ALLOPURINOL_DOSE_CHOICES)
    freq = models.CharField(max_length=50, choices=FREQ_CHOICES, default=QDAY)
    side_effects = models.CharField(
        max_length=100,
        choices=ALLOPURINOL_SIDE_EFFECT_CHOICES,
        null=True,
        blank=True,
        help_text="Have you had any side effects?",
    )
    de_sensitized = models.BooleanField(null=True, blank=True, help_text="Have you been de-sensitized to allopurinol?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=ULT)


class Febuxostat(ULTAidTreatment):
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=FEBUXOSTAT)
    brand_names = ["Uloric"]
    dose = models.IntegerField(choices=FEBUXOSTAT_DOSE_CHOICES)
    freq = models.CharField(max_length=50, choices=FREQ_CHOICES, default=QDAY)
    side_effects = models.CharField(
        max_length=100,
        choices=FEBUXOSTAT_SIDE_EFFECT_CHOICES,
        null=True,
        blank=True,
        help_text="Have you had any side effects?",
    )
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=ULT)


class Colchicine(FlareAidTreatment):
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=COLCHICINE)
    brand_names = ["Colcrys"]
    dose = models.IntegerField(choices=COLCHICINE_DOSE_CHOICES, null=True, blank=True, default=Decimal("1.2"))
    freq = models.CharField(max_length=50, choices=FREQ_CHOICES, null=True, blank=True, default=ONCE)
    dose2 = models.IntegerField(choices=COLCHICINE_DOSE_CHOICES, null=True, blank=True, default=Decimal("0.6"))
    freq2 = models.CharField(max_length=50, choices=FREQ_CHOICES, null=True, blank=True, default=ONCE)
    dose3 = models.IntegerField(choices=COLCHICINE_DOSE_CHOICES, null=True, blank=True, default=Decimal("0.6"))
    freq3 = models.CharField(max_length=50, choices=FREQ_CHOICES, null=True, blank=True, default=BID)
    duration = models.IntegerField(
        null=True, blank=True, default=7, validators=[MaxValueValidator(14), MinValueValidator(1)]
    )
    side_effects = models.CharField(
        max_length=100, choices=COLCHICINE_SIDE_EFFECT_CHOICES, blank=True, help_text="Have you had any side effects?"
    )
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=ANTIINFLAMMATORY)


class Ibuprofen(FlareAidTreatment):
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=IBUPROFEN)
    brand_names = ["Advil"]
    dose = models.IntegerField(choices=IBUPROFEN_DOSE_CHOICES, null=True, blank=True)
    freq = models.CharField(max_length=50, choices=FREQ_CHOICES, null=True, blank=True, default=QDAY)
    side_effects = models.CharField(
        max_length=100,
        choices=NSAID_SIDE_EFFECT_CHOICES,
        null=True,
        blank=True,
        help_text="Have you had any side effects?",
    )
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=NSAID)


class Naproxen(FlareAidTreatment):
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=NAPROXEN)
    brand_names = ["Aleve"]
    dose = models.IntegerField(choices=NAPROXEN_DOSE_CHOICES, null=True, blank=True)
    freq = models.CharField(max_length=50, choices=FREQ_CHOICES, null=True, blank=True, default=QDAY)
    side_effects = models.CharField(
        max_length=100, choices=NSAID_SIDE_EFFECT_CHOICES, blank=True, help_text="Have you had any side effects?"
    )
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=NSAID)


class Meloxicam(FlareAidTreatment):
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=MELOXICAM)
    brand_names = ["Mobic"]
    dose = models.DecimalField(decimal_places=1, max_digits=3, choices=MELOXICAM_DOSE_CHOICES, null=True, blank=True)
    freq = models.CharField(max_length=50, choices=FREQ_CHOICES, default=QDAY, blank=True)
    side_effects = models.CharField(
        max_length=100, choices=NSAID_SIDE_EFFECT_CHOICES, blank=True, help_text="Have you had any side effects?"
    )
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=NSAID)


class Celecoxib(FlareAidTreatment):
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=CELECOXIB)
    brand_names = ["Aleve"]
    dose = models.IntegerField(choices=CELECOXIB_DOSE_CHOICES, null=True, blank=True)
    freq = models.CharField(max_length=50, choices=FREQ_CHOICES, default=QDAY, blank=True)
    side_effects = models.CharField(
        max_length=100, choices=NSAID_SIDE_EFFECT_CHOICES, blank=True, help_text="Have you had any side effects?"
    )
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=NSAID)


class Indomethacin(FlareAidTreatment):
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=INDOMETHACIN)
    brand_names = ["Indocin"]
    dose = models.IntegerField(choices=INDOMETHACIN_DOSE_CHOICES, null=True, blank=True)
    freq = models.CharField(max_length=50, choices=FREQ_CHOICES, default=QDAY, blank=True)
    side_effects = models.CharField(
        max_length=100, choices=NSAID_SIDE_EFFECT_CHOICES, blank=True, help_text="Have you had any side effects?"
    )
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=NSAID)


class Prednisone(FlareAidTreatment):
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=PREDNISONE)
    brand_names = ["Prednisone"]
    dose = models.IntegerField(choices=PREDNISONE_DOSE_CHOICES, null=True, blank=True, default=40)
    freq = models.CharField(max_length=50, choices=FREQ_CHOICES, null=True, blank=True, default=QDAY)
    duration = models.IntegerField(
        null=True, blank=True, default=4, validators=[MaxValueValidator(14), MinValueValidator(1)]
    )
    dose2 = models.IntegerField(choices=PREDNISONE_DOSE_CHOICES, null=True, blank=True, default=20)
    freq2 = models.CharField(max_length=50, choices=FREQ_CHOICES, null=True, blank=True, default=QDAY)
    duration2 = models.IntegerField(
        null=True, blank=True, default=4, validators=[MaxValueValidator(14), MinValueValidator(1)]
    )
    side_effects = models.CharField(
        max_length=100,
        choices=PREDNISONE_SIDE_EFFECT_CHOICES,
        null=True,
        blank=True,
        help_text="Have you had any side effects?",
    )
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=SYSSTEROID)


class Methylprednisolone(FlareAidTreatment):
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=METHYLPREDNISOLONE)
    brand_names = ["Depomedrol"]
    dose = models.IntegerField(choices=METHYLPREDNISOLONE_DOSE_CHOICES, null=True, blank=True)
    freq = models.CharField(max_length=50, choices=FREQ_CHOICES, default=QDAY, blank=True)
    side_effects = models.CharField(
        max_length=100, choices=INJECTION_SIDE_EFFECT_CHOICES, blank=True, help_text="Have you had any side effects?"
    )
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=LOCSTEROID)
    as_injection = models.BooleanField(
        choices=BOOL_CHOICES,
        verbose_name="Given by joint injection?",
        help_text="Was this given by an injection into your joint?",
        default=False,
        blank=True,
        null=True,
    )

    def __str__(self):
        if self.as_injection == True:
            return f'{str(self.generic_name) + " " + str(self.dose) + " mg injection"}'
        elif self.dose:
            return f'{str(self.generic_name) + " " + str(self.dose) + " mg " + str(self.freq)}'
        else:
            return f'{str(self.generic_name) + " dose not recorded"}'


class Probenecid(ULTAidTreatment):
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=PROBENECID)
    brand_names = ["Probalan"]
    dose = models.IntegerField(choices=PROBENECID_DOSE_CHOICES)
    freq = models.CharField(max_length=50, choices=FREQ_CHOICES, default=BID)
    side_effects = models.CharField(
        max_length=100,
        choices=PROBENECID_SIDE_EFFECT_CHOICES,
        null=True,
        blank=True,
        help_text="Have you had any side effects?",
    )
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=URATEEXCRETAGOGUE)


class Tinctureoftime(FlareAidTreatment):
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=TINCTUREOFTIME)
    brand_names = ["Tincture of time"]
    duration = models.IntegerField(help_text="How long did it take to get better?", null=True, blank=True)
    dose = models.IntegerField(blank=True, null=True, help_text="Any optional information on your dose?")
    freq = models.CharField(
        max_length=50,
        choices=FREQ_CHOICES,
        default=QDAY,
        null=True,
        blank=True,
        help_text="Any optional information on your frequency?",
    )
    side_effects = models.CharField(
        max_length=400, null=True, blank=True, help_text="Have you had any side effects? Please list"
    )
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=TINCTUREOFTIME)

    def __str__(self):
        return f'{"Tincture of time for: " + str(self.duration) + " days"}'


class Othertreat(FlareAidTreatment):
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=OTHER)
    brand_names = ["Other"]
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    dose = models.IntegerField(blank=True, null=True, help_text="Any optional information on your dose?")
    freq = models.CharField(
        max_length=50,
        choices=FREQ_CHOICES,
        default=QDAY,
        null=True,
        blank=True,
        help_text="Any optional information on your frequency?",
    )
    side_effects = models.CharField(max_length=400, blank=True, help_text="Have you had any side effects? Please list")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=OTHER)

    def __str__(self):
        return self.name
