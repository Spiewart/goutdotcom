from autoslug import AutoSlugField
from django.db import models
from django.conf import settings
from django_extensions.db.models import TimeStampedModel
from django.urls import reverse

import datetime
from decimal import *

BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))

ALLOPURINOL = 'allopurinol'
FEBUXOSTAT = 'febuxostat'
PREDNISONE = 'prednisone'
COLCHICINE = 'colchicine'
PROBENECID = 'probenecid'
PEGLOTICASE = 'pegloticase'
IBUPROFEN = 'ibuprofen'
NAPROXEN = 'naproxen'
MELOXICAM = 'meloxicam'
CELECOXIB = 'celecoxib'
METHYLPREDNISOLONE = 'methylprednisolone'

ULT = 'urate-lowering therapy'
SYSSTEROID = 'systemic steroid'
ANTIINFLAMMATORY = 'anti-inflammatory'
NSAID = 'nonsteroidal antiinflammatory drug'
URATEEXCRETAGOGUE = 'urate extreagogue'
LOCSTEROID = 'local steroid'
URICASE = 'recombinant uricase'

QDAY = 'qday'
BID = 'bid'
TID = 'tid'
QDAYPRN = 'qday prn'
BIDPRN = 'bid prn'
QTWOWEEK = 'q2weeks'
ONCE = 'once'

MEDICATION_CHOICES = (
    (ALLOPURINOL, 'Allopurinol'),
    (FEBUXOSTAT, 'Febuxostat'),
    (PREDNISONE, 'Prednisone'),
    (COLCHICINE, 'Colchicine'),
    (PROBENECID, 'Probenecid'),
    (PEGLOTICASE, 'Pegloticase'),
    (IBUPROFEN, 'Ibuprofen'),
    (NAPROXEN, 'Naproxen'),
    (MELOXICAM, 'Meloxicam'),
    (CELECOXIB, 'Celecoxib'),
    (METHYLPREDNISOLONE, 'Methylprednisolone'),
)

DRUG_CLASS_CHOICES = (
    (ULT, 'Urate-lowering therapy'),
    (SYSSTEROID, 'Systemic steroid'),
    (ANTIINFLAMMATORY, 'Anti-inflammatory'),
    (NSAID, 'Nonsteroidal anti-inflammatory drug'),
    (URATEEXCRETAGOGUE, 'Urate excretagogue'),
    (LOCSTEROID, 'Local steroid'),
    (URICASE, 'Recombinant uricase'),
)

FREQ_CHOICES = (
    (QDAY, 'Once daily'),
    (BID, 'Twice daily'),
    (TID, 'Three times daily'),
    (QDAYPRN, 'Once daily as needed'),
    (BIDPRN, 'Twice daily as needed'),
    (QTWOWEEK, 'Every 2 weeks'),
    (ONCE, 'Once'),
)

ALLOPURINOL_DOSE_CHOICES = ()

FEBUXOSTAT_DOSE_CHOICES = ()

for x in range(1, 7):
    y = x * 20
    z = str(y) + " mg"
    FEBUXOSTAT_DOSE_CHOICES += (y, z),

for x in range(1, 19):
    y = x*50
    z = str(y) + " mg"
    ALLOPURINOL_DOSE_CHOICES += (y, z),

COLCHICINE_DOSE_CHOICES = (
    (.6, '0.6 mg'),
)

PROBENECID_DOSE_CHOICES = (
    (250, '250 mg'),
    (500, '500 mg'),
    (750, '750 mg'),
    (1000, '1000 mg'),
)

IBUPROFEN_DOSE_CHOICES = (
    (200, '200 mg'),
    (400, '400 mg'),
    (600, '600 mg'),
    (800, '800 mg'),
)

NAPROXEN_DOSE_CHOICES = (
    (220, '220 mg'),
    (250, '250 mg'),
    (440, '440 mg'),
    (500, '500 mg'),
)

MELOXICAM_DOSE_CHOICES = (
    (7.5, '7.5 mg'),
    (15, '15 mg'),
)

CELECOXIB_DOSE_CHOICES = (
    (200, '200 mg'),
    (400, '400 mg'),
)

METHYLPREDNISOLONE_DOSE_CHOICES = (
    (20, '20 mg'),
    (40, '40 mg'),
    (80, '80 mg'),
)

ALLOPURINOL_SIDE_EFFECT_CHOICES = (
    ('Rash', 'Rash'),
    ('Hypersensitivity syndrome', 'Hypersensitivity syndrome'),
    ('Elevated LFTs', 'Elevated LFTs'),
    ('Cytopenias', 'Cytopenias'),
    ('GI upset', 'GI upset'),
)

FEBUXOSTAT_SIDE_EFFECT_CHOICES = (
    ('Rash', 'Rash'),
    ('Hypersensitivity syndrome', 'Hypersensitivity syndrome'),
    ('Elevated LFTs', 'Elevated LFTs'),
    ('Cytopenias', 'Cytopenias'),
    ('GI upset', 'GI upset'),
)

COLCHICINE_SIDE_EFFECT_CHOICES = (
    ('GI upset', 'GI upset'),
    ('Medication interaction', 'Medication interaction'),
)

NSAID_SIDE_EFFECT_CHOICES = (
    ('Rash', 'Rash'),
    ('Kidney failure', 'Kidney failure'),
    ('Stomach ulcer', 'Stomach ulcer'),
    ('GI upset', 'GI upset'),
    ('Medication interaction', 'Medication interaction'),
)

PREDNISONE_SIDE_EFFECT_CHOICES = (
    ('Insomnia', 'Insomnia'),
    ('Weight gain', 'Weight gain'),
    ('Anxiety', 'Anxiety'),
    ('Hyperglycemia', 'Hyperglycemia'),
    ('Weakness', 'Weakness'),
    ('Easy bruising', 'Easy bruising'),
    ('Osteoporosis', 'Osteoporosis'),
    ('Cataract', 'Cataract'),
    ('Infection', 'Infection'),
)

INJECTION_SIDE_EFFECT_CHOICES = (
    ('Bleeding', 'Bleeding'),
    ('Infection', 'Infection'),
)

PROBENECID_SIDE_EFFECT_CHOICES = (
    ('Flushing', 'Flushing'),
    ('Headache', 'Headache'),
)

# Create your models here.
class Allopurinol(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=ALLOPURINOL)
    brand_names = ["Xyloprim", "Aloprim"]
    dose = models.IntegerField(choices=ALLOPURINOL_DOSE_CHOICES)
    freq = models.CharField(max_length = 50, choices=FREQ_CHOICES, default=QDAY)
    date_started = models.DateField(default=datetime.datetime.now)
    date_ended = models.DateField(null=True, blank=True)
    side_effects = models.CharField(max_length=100, choices=ALLOPURINOL_SIDE_EFFECT_CHOICES, null=True, blank=True, help_text="Have you had any side effects?")
    de_sensitized = models.BooleanField(null=True, blank=True, help_text="Have you been de-sensitized to allopurinol?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=ULT)

    class Meta:
        pass

    def __str__(self):
        return f'{str(self.generic_name) + " " + str(self.dose) + " mg " + str(self.freq)}'

    def get_absolute_url(self):
        return reverse("treatment:allopurinol-detail", kwargs={"pk":self.pk})

class Febuxostat(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=FEBUXOSTAT)
    brand_names = ["Uloric"]
    dose = models.IntegerField(choices=FEBUXOSTAT_DOSE_CHOICES)
    freq = models.CharField(max_length = 50, choices=FREQ_CHOICES, default=QDAY)
    date_started = models.DateField(default=datetime.datetime.now)
    date_ended = models.DateField(null=True, blank=True)
    side_effects = models.CharField(max_length=100, choices=FEBUXOSTAT_SIDE_EFFECT_CHOICES, null=True, blank=True, help_text="Have you had any side effects?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=ULT)

    class Meta:
        pass

    def __str__(self):
        return f'{str(self.generic_name) + " " + str(self.dose) + " mg " + str(self.freq)}'

    def get_absolute_url(self):
        return reverse("treatment:febuxostat-detail",  kwargs={"pk": self.pk})

class Colchicine(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=COLCHICINE)
    brand_names = ["Colcrys"]
    dose = models.DecimalField(decimal_places=1, max_digits=2, default=0.6)
    freq = models.CharField(max_length = 50, choices=FREQ_CHOICES, default=QDAY)
    date_started = models.DateField(default=datetime.datetime.now)
    date_ended = models.DateField(null=True, blank=True)
    side_effects = models.CharField(max_length=100, choices=COLCHICINE_SIDE_EFFECT_CHOICES, null=True, blank=True, help_text="Have you had any side effects?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=ANTIINFLAMMATORY)
    as_prophylaxis = models.BooleanField(choices=BOOL_CHOICES, verbose_name="Flare prophylaxis?",
                                         help_text="Is this for flare prophylaxis while initiating ULT?", default=False)
    
    def duration_calc(self):
        if self.date_started:
            if self.date_ended:
                duration = self.date_ended - self.date_started
                return duration
                
    class Meta:
        pass

    def __str__(self):
        return f'{str(self.generic_name) + " " + str(self.dose) + " mg " + str(self.freq)}'

    def get_absolute_url(self):
        return reverse("treatment:colchicine-detail",  kwargs={"pk": self.pk})

class Ibuprofen(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=IBUPROFEN)
    brand_names = ["Advil"]
    dose = models.IntegerField(choices=IBUPROFEN_DOSE_CHOICES)
    freq = models.CharField(max_length = 50, choices=FREQ_CHOICES, default=QDAY)
    date_started = models.DateField(default=datetime.datetime.now)
    date_ended = models.DateField(null=True, blank=True)
    side_effects = models.CharField(max_length=100, choices=NSAID_SIDE_EFFECT_CHOICES, null=True, blank=True, help_text="Have you had any side effects?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=NSAID)
    as_prophylaxis = models.BooleanField(choices=BOOL_CHOICES, verbose_name="Flare prophylaxis?",
                                         help_text="Is this for flare prophylaxis while initiating ULT?", default=False)

    class Meta:
        pass

    def __str__(self):
        return f'{str(self.generic_name) + " " + str(self.dose) + " mg " + str(self.freq)}'

    def get_absolute_url(self):
        return reverse("treatment:ibuprofen-detail",  kwargs={"pk": self.pk})

class Naproxen(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=NAPROXEN)
    brand_names = ["Aleve"]
    dose = models.IntegerField(choices=NAPROXEN_DOSE_CHOICES)
    freq = models.CharField(max_length = 50, choices=FREQ_CHOICES, default=QDAY)
    date_started = models.DateField(default=datetime.datetime.now)
    date_ended = models.DateField(null=True, blank=True)
    side_effects = models.CharField(max_length=100, choices=NSAID_SIDE_EFFECT_CHOICES, null=True, blank=True, help_text="Have you had any side effects?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=NSAID)
    as_prophylaxis = models.BooleanField(choices=BOOL_CHOICES, verbose_name="Flare prophylaxis?",
                                         help_text="Is this for flare prophylaxis while initiating ULT?", default=False)

    class Meta:
        pass

    def __str__(self):
        return f'{str(self.generic_name) + " " + str(self.dose) + " mg " + str(self.freq)}'

    def get_absolute_url(self):
        return reverse("treatment:naproxen-detail",  kwargs={"pk": self.pk})

class Meloxicam(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=MELOXICAM)
    brand_names = ["Mobic"]
    dose = models.IntegerField(choices=MELOXICAM_DOSE_CHOICES)
    freq = models.CharField(max_length = 50, choices=FREQ_CHOICES, default=QDAY)
    date_started = models.DateField(default=datetime.datetime.now)
    date_ended = models.DateField(null=True, blank=True)
    side_effects = models.CharField(max_length=100, choices=NSAID_SIDE_EFFECT_CHOICES, null=True, blank=True, help_text="Have you had any side effects?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=NSAID)
    as_prophylaxis = models.BooleanField(choices=BOOL_CHOICES, verbose_name="Flare prophylaxis?",
                                         help_text="Is this for flare prophylaxis while initiating ULT?", default=False)

    class Meta:
        pass

    def __str__(self):
        return f'{str(self.generic_name) + " " + str(self.dose) + " mg " + str(self.freq)}'

    def get_absolute_url(self):
        return reverse("treatment:meloxicam-detail",  kwargs={"pk": self.pk})

class Celecoxib(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=CELECOXIB)
    brand_names = ["Aleve"]
    dose = models.IntegerField(choices=CELECOXIB_DOSE_CHOICES)
    freq = models.CharField(max_length = 50, choices=FREQ_CHOICES, default=QDAY)
    date_started = models.DateField(default=datetime.datetime.now)
    date_ended = models.DateField(null=True, blank=True)
    side_effects = models.CharField(max_length=100, choices=NSAID_SIDE_EFFECT_CHOICES, null=True, blank=True, help_text="Have you had any side effects?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=NSAID)
    as_prophylaxis = models.BooleanField(choices=BOOL_CHOICES, verbose_name="Flare prophylaxis?",
                                         help_text="Is this for flare prophylaxis while initiating ULT?", default=False)

    class Meta:
        pass

    def __str__(self):
        return f'{str(self.generic_name) + " " + str(self.dose) + " mg " + str(self.freq)}'

    def get_absolute_url(self):
        return reverse("treatment:celecoxib-detail",  kwargs={"pk": self.pk})


class Prednisone(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=PREDNISONE)
    brand_names = ["Prednisone"]
    dose = models.IntegerField()
    freq = models.CharField(max_length=50, choices=FREQ_CHOICES, default=QDAY)
    date_started = models.DateField(default=datetime.datetime.now)
    date_ended = models.DateField(null=True, blank=True)
    side_effects = models.CharField(max_length=100, choices=PREDNISONE_SIDE_EFFECT_CHOICES,
                                    null=True, blank=True, help_text="Have you had any side effects?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=SYSSTEROID)
    as_prophylaxis = models.BooleanField(choices=BOOL_CHOICES, verbose_name="Flare prophylaxis?",
                                         help_text="Is this for flare prophylaxis while initiating ULT?", default=False)

    class Meta:
        pass

    def __str__(self):
        return f'{str(self.generic_name) + " " + str(self.dose) + " mg " + str(self.freq)}'

    def get_absolute_url(self):
        return reverse("treatment:prednisone-detail",  kwargs={"pk": self.pk})

class Methylprednisolone(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=METHYLPREDNISOLONE)
    brand_names = ["Depomedrol"]
    dose = dose = models.IntegerField(choices=METHYLPREDNISOLONE_DOSE_CHOICES)
    freq = models.CharField(max_length=50, choices=FREQ_CHOICES, default=QDAY)
    date_started = models.DateField(default=datetime.datetime.now)
    date_ended = models.DateField(null=True, blank=True)
    side_effects = models.CharField(max_length=100, choices=INJECTION_SIDE_EFFECT_CHOICES,
                                    null=True, blank=True, help_text="Have you had any side effects?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=LOCSTEROID)
    as_injection = models.BooleanField(choices=BOOL_CHOICES, verbose_name="Given by joint injection?",
                                                        help_text="Was this given by an injection into your joint?", default=False)
    class Meta:
        pass

    def __str__(self):
        return f'{str(self.generic_name) + " " + str(self.dose) + " mg " + str(self.freq)}'

    def get_absolute_url(self):
        return reverse("treatment:methylprednisolone-detail",  kwargs={"pk": self.pk})

class Probenecid(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=PROBENECID)
    brand_names = ["Probalan"]
    dose = dose = models.IntegerField(choices=PROBENECID_DOSE_CHOICES)
    freq = models.CharField(max_length=50, choices=FREQ_CHOICES, default=BID)
    date_started = models.DateField(default=datetime.datetime.now)
    date_ended = models.DateField(null=True, blank=True)
    side_effects = models.CharField(max_length=100, choices=PROBENECID_SIDE_EFFECT_CHOICES,
                                    null=True, blank=True, help_text="Have you had any side effects?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=URATEEXCRETAGOGUE)

    class Meta:
        pass

    def __str__(self):
        return f'{str(self.generic_name) + " " + str(self.dose) + " mg " + str(self.freq)}'

    def get_absolute_url(self):
        return reverse("treatment:probenecid-detail",  kwargs={"pk": self.pk})
