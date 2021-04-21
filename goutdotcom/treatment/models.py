from autoslug import AutoSlugField
from django.db import models
from django.conf import settings
from django_extensions.db.models import TimeStampedModel
from django.urls import reverse

import datetime
from decimal import *

ALLOPURINOL = 'allopurinol'
FEBUXOSTAT = 'febuxostat'
PREDNISONE = 'prednisone'
COLCHICINE = 'colchicine'
PROBENACID = 'probenacid'
PEGLOTICASE = 'pegloticase'
IBUPROFEN = 'ibuprofen'
NAPROXEN = 'naproxen'
MELOXICAM = 'meloxicam'
CELECOXIB = 'celecoxib'

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

MEDICATION_CHOICES = (
    (ALLOPURINOL, 'Allopurinol'),
    (FEBUXOSTAT, 'Febuxostat'),
    (PREDNISONE, 'Prednisone'),
    (COLCHICINE, 'Colchicine'),
    (PROBENACID, 'Probenacid'),
    (PEGLOTICASE, 'Pegloticase'),
    (IBUPROFEN, 'Ibuprofen'),
    (NAPROXEN, 'Naproxen'),
    (MELOXICAM, 'Meloxicam'),
    (CELECOXIB, 'Celecoxib'),
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
    (Decimal('0.6'), '0.6 mg'),
)

PROBENACID_DOSE_CHOICES = (
    ('250', '250 mg'),
    ('500', '500 mg'),
    ('750', '750 mg'),
    ('1000', '1000 mg'),
)

IBUPROFEN_DOSE_CHOICES = (
    ('200', '200 mg'),
    ('400', '400 mg'),
    ('600', '600 mg'),
    ('800', '800 mg'),
)

NAPROXEN_DOSE_CHOICES = (
    ('220', '220 mg'),
    ('250', '250 mg'),
    ('440', '440 mg'),
    ('500', '500 mg'),
)

MELOXICAM_DOSE_CHOICES = (
    ('7.5', '7.5 mg'),
    ('15', '15 mg'),
)

CELECOXIB_DOSE_CHOICES = (
    ('200', '200 mg'),
    ('400', '400 mg'),
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

# Create your models here.
class Allopurinol(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=ALLOPURINOL)
    med_slug = AutoSlugField(
        "Medication Name", unique_with="user", always_update=False, populate_from="generic_name"
    )
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
        return reverse("treatment:allopurinol-detail", kwargs={"slug":self.med_slug})

class Febuxostat(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    ) 
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=FEBUXOSTAT)
    med_slug = AutoSlugField(
        "Medication Name", unique_with="user", always_update=False, populate_from="generic_name"
    )
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
        return reverse("treatment:detail", kwargs={"slug":self.med_slug})

class Colchicine(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=COLCHICINE)
    med_slug = AutoSlugField(
        "Medication Name", unique=True, always_update=False, populate_from="generic_name"
    )
    brand_names = ["Colcrys"]
    dose = models.IntegerField(choices=COLCHICINE_DOSE_CHOICES)
    freq = models.CharField(max_length = 50, choices=FREQ_CHOICES, default=QDAY)
    date_started = models.DateField(default=datetime.datetime.now)
    date_ended = models.DateField(null=True, blank=True)
    side_effects = models.CharField(max_length=100, choices=COLCHICINE_SIDE_EFFECT_CHOICES, null=True, blank=True, help_text="Have you had any side effects?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=ANTIINFLAMMATORY)

    class Meta:
        pass

    def __str__(self):
        return f'{str(self.generic_name) + " " + str(self.dose) + " mg " + str(self.freq)}'
    
    def get_absolute_url(self):
        return reverse("treatment:detail", kwargs={"slug":self.med_slug})

class Ibuprofen(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=IBUPROFEN)
    med_slug = AutoSlugField(
        "Medication Name", unique=True, always_update=False, populate_from="generic_name"
    )
    brand_names = ["Advil"]
    dose = models.IntegerField(choices=IBUPROFEN_DOSE_CHOICES)
    freq = models.CharField(max_length = 50, choices=FREQ_CHOICES, default=QDAY)
    date_started = models.DateField(default=datetime.datetime.now)
    date_ended = models.DateField(null=True, blank=True)
    side_effects = models.CharField(max_length=100, choices=NSAID_SIDE_EFFECT_CHOICES, null=True, blank=True, help_text="Have you had any side effects?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=NSAID)

    class Meta:
        pass

    def __str__(self):
        return f'{str(self.generic_name) + " " + str(self.dose) + " mg " + str(self.freq)}'
    
    def get_absolute_url(self):
        return reverse("treatment:detail", kwargs={"slug":self.med_slug})

class Naproxen(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )    
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=NAPROXEN)
    med_slug = AutoSlugField(
        "Medication Name", unique=True, always_update=False, populate_from="generic_name"
    )
    brand_names = ["Aleve"]
    dose = models.IntegerField(choices=NAPROXEN_DOSE_CHOICES)
    freq = models.CharField(max_length = 50, choices=FREQ_CHOICES, default=QDAY)
    date_started = models.DateField(default=datetime.datetime.now)
    date_ended = models.DateField(null=True, blank=True)
    side_effects = models.CharField(max_length=100, choices=NSAID_SIDE_EFFECT_CHOICES, null=True, blank=True, help_text="Have you had any side effects?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=NSAID)

    class Meta:
        pass

    def __str__(self):
        return f'{str(self.generic_name) + " " + str(self.dose) + " mg " + str(self.freq)}'
    
    def get_absolute_url(self):
        return reverse("treatment:detail", kwargs={"slug":self.med_slug})

class Meloxicam(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=MELOXICAM)
    med_slug = AutoSlugField(
        "Medication Name", unique=True, always_update=False, populate_from="generic_name"
    )
    brand_names = ["Aleve"]
    dose = models.IntegerField(choices=MELOXICAM_DOSE_CHOICES)
    freq = models.CharField(max_length = 50, choices=FREQ_CHOICES, default=QDAY)
    date_started = models.DateField(default=datetime.datetime.now)
    date_ended = models.DateField(null=True, blank=True)
    side_effects = models.CharField(max_length=100, choices=NSAID_SIDE_EFFECT_CHOICES, null=True, blank=True, help_text="Have you had any side effects?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=NSAID)

    class Meta:
        pass

    def __str__(self):
        return f'{str(self.generic_name) + " " + str(self.dose) + " mg " + str(self.freq)}'
    
    def get_absolute_url(self):
        return reverse("treatment:detail", kwargs={"slug":self.med_slug})

class Celecoxib(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )    
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=CELECOXIB)
    med_slug = AutoSlugField(
        "Medication Name", unique=True, always_update=False, populate_from="generic_name"
    )   
    brand_names = ["Aleve"]
    dose = models.IntegerField(choices=CELECOXIB_DOSE_CHOICES)
    freq = models.CharField(max_length = 50, choices=FREQ_CHOICES, default=QDAY)
    date_started = models.DateField(default=datetime.datetime.now)
    date_ended = models.DateField(null=True, blank=True)
    side_effects = models.CharField(max_length=100, choices=NSAID_SIDE_EFFECT_CHOICES, null=True, blank=True, help_text="Have you had any side effects?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=NSAID)

    class Meta:
        pass

    def __str__(self):
        return f'{str(self.generic_name) + " " + str(self.dose) + " mg " + str(self.freq)}'
    
    def get_absolute_url(self):
        return reverse("treatment:detail", kwargs={"slug":self.med_slug})