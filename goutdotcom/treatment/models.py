from django.db import models
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

COLCHICINE_DOSE_CHOICES = (
    (Decimal('0.6'), '0.6 mg'),
)

PROBENACID_DOSE_CHOICES = (
    ('250', '250 mg'),
    ('500', '500 mg'),
    ('750', '750 mg'),
    ('1000', '1000 mg'),
)

# Create your models here.
class Medication(models.Model):
    date_started = models.DateField(default=datetime.datetime.now)
    date_ended = models.DateField(null=True, blank=True)
    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES)
    freq = models.CharField(max_length = 50, choices=FREQ_CHOICES, default=QDAY)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{str(self.generic_name) + " " + str(self.dose) + " mg " + str(self.freq)}'

class Allopurinol(Medication):
    ALLOPURINOL_DOSE_CHOICES = ()

    for x in range(1, 19):
        y = x*50
        z = str(y) + " mg"
        ALLOPURINOL_DOSE_CHOICES += (y, z),

    SIDE_EFFECT_CHOICES = (
        ('rash', 'rash'),
        ('Hypersensitivity syndrome', 'Hypersensitivity syndrome'),
        ('Elevated LFTs', 'Elevated LFTs'),
        ('Cytopenias', 'Cytopenias'),
        ('GI upset', 'GI upset'),
    )

    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=ALLOPURINOL)
    brand_names = ["Xyloprim", "Aloprim"]
    dose = models.IntegerField(choices=ALLOPURINOL_DOSE_CHOICES)
    side_effects = models.CharField(max_length=100, choices=SIDE_EFFECT_CHOICES, null=True, blank=True, help_text="Have you had any side effects?")
    de_sensitized = models.BooleanField(null=True, blank=True, help_text="Have you been de-sensitized to allopurinol?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=ULT)

class Febuxostat(Medication):
    FEBUXOSTAT_DOSE_CHOICES = ()

    for x in range(1, 7):
        y = x * 20
        z = str(y) + " mg"
        FEBUXOSTAT_DOSE_CHOICES += (y, z),

    SIDE_EFFECT_CHOICES = (
        ('rash', 'rash'),
        ('Hypersensitivity syndrome', 'Hypersensitivity syndrome'),
        ('Elevated LFTs', 'Elevated LFTs'),
        ('Cytopenias', 'Cytopenias'),
        ('GI upset', 'GI upset'),
    )

    generic_name = models.CharField(max_length=60, choices=MEDICATION_CHOICES, default=FEBUXOSTAT)
    brand_names = ["Uloric"]
    dose = models.IntegerField(choices=FEBUXOSTAT_DOSE_CHOICES)
    side_effects = models.CharField(max_length=100, choices=SIDE_EFFECT_CHOICES, null=True, blank=True, help_text="Have you had any side effects?")
    drug_class = models.CharField(max_length=50, choices=DRUG_CLASS_CHOICES, default=ULT)