from django.db import models
from django.conf import settings
from django_extensions.db.models import TimeStampedModel
from django.urls import reverse

import datetime
from decimal import *

from .choices import *

# Create your models here.
class Treatment(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES)
    brand_names = [""]
    dose = models.IntegerField()
    freq = models.CharField(max_length=50, choices=FREQ_CHOICES)
    date_started = models.DateField(default=datetime.datetime.now)
    date_ended = models.DateField(null=True, blank=True)
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
        return reverse("treatment:detail",  kwargs={"pk": self.pk, "treatment":self.generic_name})

    def __unicode__(self):
        return self.generic_name

class TemporizingTreatment(Treatment):
    date_started = models.DateField(default=datetime.datetime.now, blank=True, null=True)
    prn = models.BooleanField(choices=BOOL_CHOICES, default=True, null=True, blank=True, help_text="Do you take this medication only as needed (PRN)?")
    as_prophylaxis = models.BooleanField(choices=BOOL_CHOICES, verbose_name="Flare prophylaxis?", help_text="Is this for flare prophylaxis while initiating ULT?", default=False, blank=True, null=True)

    def duration_calc(self):
        if self.date_started:
            if self.date_ended:
                duration = self.date_ended - self.date_started
                return duration

    class Meta:
        abstract = True

class Allopurinol(Treatment):
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=ALLOPURINOL)
    brand_names = ["Xyloprim", "Aloprim"]
    dose = models.IntegerField(choices=ALLOPURINOL_DOSE_CHOICES)
    freq = models.CharField(max_length = 50, choices=FREQ_CHOICES, default=QDAY)
    side_effects = models.CharField(max_length=100, choices=ALLOPURINOL_SIDE_EFFECT_CHOICES, null=True, blank=True, help_text="Have you had any side effects?")
    de_sensitized = models.BooleanField(null=True, blank=True, help_text="Have you been de-sensitized to allopurinol?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=ULT)

class Febuxostat(Treatment):
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=FEBUXOSTAT)
    brand_names = ["Uloric"]
    dose = models.IntegerField(choices=FEBUXOSTAT_DOSE_CHOICES)
    freq = models.CharField(max_length = 50, choices=FREQ_CHOICES, default=QDAY)
    side_effects = models.CharField(max_length=100, choices=FEBUXOSTAT_SIDE_EFFECT_CHOICES, null=True, blank=True, help_text="Have you had any side effects?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=ULT)

class Colchicine(TemporizingTreatment):
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=COLCHICINE)
    brand_names = ["Colcrys"]
    dose = models.DecimalField(decimal_places=1, max_digits=2, choices=COLCHICINE_DOSE_CHOICES, null=True, blank=True)
    freq = models.CharField(max_length = 50, choices=FREQ_CHOICES, default=QDAY, blank=True)
    side_effects = models.CharField(max_length=100, choices=COLCHICINE_SIDE_EFFECT_CHOICES, blank=True, help_text="Have you had any side effects?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=ANTIINFLAMMATORY)

class Ibuprofen(TemporizingTreatment):
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=IBUPROFEN)
    brand_names = ["Advil"]
    dose = models.IntegerField(choices=IBUPROFEN_DOSE_CHOICES, null=True, blank=True)
    freq = models.CharField(max_length = 50, choices=FREQ_CHOICES, default=QDAY, blank=True)
    side_effects = models.CharField(max_length=100, choices=NSAID_SIDE_EFFECT_CHOICES, null=True, blank=True, help_text="Have you had any side effects?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=NSAID)

class Naproxen(TemporizingTreatment):
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=NAPROXEN)
    brand_names = ["Aleve"]
    dose = models.IntegerField(choices=NAPROXEN_DOSE_CHOICES, null=True, blank=True)
    freq = models.CharField(max_length = 50, choices=FREQ_CHOICES, default=QDAY, blank=True)
    side_effects = models.CharField(max_length=100, choices=NSAID_SIDE_EFFECT_CHOICES, blank=True, help_text="Have you had any side effects?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=NSAID)

class Meloxicam(TemporizingTreatment):
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=MELOXICAM)
    brand_names = ["Mobic"]
    dose = models.DecimalField(decimal_places=1, max_digits=3, choices=MELOXICAM_DOSE_CHOICES, null=True, blank=True)
    freq = models.CharField(max_length = 50, choices=FREQ_CHOICES, default=QDAY, blank=True)
    side_effects = models.CharField(max_length=100, choices=NSAID_SIDE_EFFECT_CHOICES, blank=True, help_text="Have you had any side effects?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=NSAID)

class Celecoxib(TemporizingTreatment):
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=CELECOXIB)
    brand_names = ["Aleve"]
    dose = models.IntegerField(choices=CELECOXIB_DOSE_CHOICES, null=True, blank=True)
    freq = models.CharField(max_length = 50, choices=FREQ_CHOICES, default=QDAY, blank=True)
    side_effects = models.CharField(max_length=100, choices=NSAID_SIDE_EFFECT_CHOICES, blank=True, help_text="Have you had any side effects?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=NSAID)

class Prednisone(TemporizingTreatment):
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=PREDNISONE)
    brand_names = ["Prednisone"]
    dose = models.IntegerField(null=True, blank=True)
    freq = models.CharField(max_length=50, choices=FREQ_CHOICES, default=QDAY, blank=True)
    side_effects = models.CharField(max_length=100, choices=PREDNISONE_SIDE_EFFECT_CHOICES,
                                    null=True, blank=True, help_text="Have you had any side effects?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=SYSSTEROID)

class Methylprednisolone(TemporizingTreatment):
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=METHYLPREDNISOLONE)
    brand_names = ["Depomedrol"]
    dose = models.IntegerField(choices=METHYLPREDNISOLONE_DOSE_CHOICES, null=True, blank=True)
    freq = models.CharField(max_length=50, choices=FREQ_CHOICES, default=QDAY, blank=True)
    side_effects = models.CharField(max_length=100, choices=INJECTION_SIDE_EFFECT_CHOICES,
                                    blank=True, help_text="Have you had any side effects?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=LOCSTEROID)
    as_injection = models.BooleanField(choices=BOOL_CHOICES, verbose_name="Given by joint injection?",
                                                        help_text="Was this given by an injection into your joint?", default=False, blank=True, null=True)

    def __str__(self):
        if self.as_injection == True:
            return f'{str(self.generic_name) + " " + str(self.dose) + " mg injection"}'
        elif self.dose:
            return f'{str(self.generic_name) + " " + str(self.dose) + " mg " + str(self.freq)}'
        else:
            return f'{str(self.generic_name) + " dose not recorded"}'
class Probenecid(Treatment):
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=PROBENECID)
    brand_names = ["Probalan"]
    dose = models.IntegerField(choices=PROBENECID_DOSE_CHOICES)
    freq = models.CharField(max_length=50, choices=FREQ_CHOICES, default=BID)
    side_effects = models.CharField(max_length=100, choices=PROBENECID_SIDE_EFFECT_CHOICES,
                                    null=True, blank=True, help_text="Have you had any side effects?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=URATEEXCRETAGOGUE)

class Tinctureoftime(TemporizingTreatment):
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=TINCTUREOFTIME)
    brand_names = ["Tincture of time"]
    duration = models.IntegerField(help_text="How long did it take to get better?", null=True, blank=True)
    dose = models.IntegerField(blank=True, null=True, help_text="Any optional information on your dose?")
    freq = models.CharField(max_length=50, choices=FREQ_CHOICES, default=QDAY, null=True,
                            blank=True, help_text="Any optional information on your frequency?")
    side_effects = models.CharField(max_length=400, null=True, blank=True, help_text="Have you had any side effects? Please list")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=TINCTUREOFTIME)

    def __str__(self):
        return f'{"Tincture of time for: " + str(self.duration) + " days"}'

class Othertreat(TemporizingTreatment):
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=OTHER)
    brand_names = ["Other"]
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    dose = models.IntegerField(blank=True, null=True, help_text="Any optional information on your dose?")
    freq = models.CharField(max_length=50, choices=FREQ_CHOICES, default=QDAY, null=True, blank=True, help_text="Any optional information on your frequency?")
    side_effects = models.CharField(max_length=400, blank=True, help_text="Have you had any side effects? Please list")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=OTHER)

    def __str__(self):
        return self.name
