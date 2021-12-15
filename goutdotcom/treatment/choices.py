from decimal import *

BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))

ALLOPURINOL = 'allopurinol'
FEBUXOSTAT = 'febuxostat'
INDOMETHACIN = "indomethacin"
PREDNISONE = 'prednisone'
COLCHICINE = 'colchicine'
PROBENECID = 'probenecid'
PEGLOTICASE = 'pegloticase'
IBUPROFEN = 'ibuprofen'
NAPROXEN = 'naproxen'
MELOXICAM = 'meloxicam'
CELECOXIB = 'celecoxib'
METHYLPREDNISOLONE = 'methylprednisolone'
TINCTUREOFTIME = 'tinctureoftime'
OTHER = 'other'

ULT = 'urate-lowering therapy'
SYSSTEROID = 'systemic steroid'
ANTIINFLAMMATORY = 'anti-inflammatory'
NSAID = 'nonsteroidal anti-inflammatory drug'
URATEEXCRETAGOGUE = 'urate extreagogue'
LOCSTEROID = 'local steroid'
URICASE = 'recombinant uricase'

QDAY = 'qday'
BID = 'bid'
TID = 'tid'
QTWOWEEK = 'q2weeks'
ONCE = 'once'

MEDICATION_CHOICES = (
    (ALLOPURINOL, 'Allopurinol'),
    (FEBUXOSTAT, 'Febuxostat'),
    (INDOMETHACIN, "Indomethacin"),
    (PREDNISONE, 'Prednisone'),
    (COLCHICINE, 'Colchicine'),
    (PROBENECID, 'Probenecid'),
    (PEGLOTICASE, 'Pegloticase'),
    (IBUPROFEN, 'Ibuprofen'),
    (NAPROXEN, 'Naproxen'),
    (MELOXICAM, 'Meloxicam'),
    (CELECOXIB, 'Celecoxib'),
    (METHYLPREDNISOLONE, 'Methylprednisolone'),
    (TINCTUREOFTIME, 'Tinctureoftime'),
    (OTHER, 'Other'),
)

DRUG_CLASS_CHOICES = (
    (ULT, 'Urate-lowering therapy'),
    (SYSSTEROID, 'Systemic steroid'),
    (ANTIINFLAMMATORY, 'Anti-inflammatory'),
    (NSAID, 'Nonsteroidal anti-inflammatory drug'),
    (URATEEXCRETAGOGUE, 'Urate excretagogue'),
    (LOCSTEROID, 'Local steroid'),
    (URICASE, 'Recombinant uricase'),
    (OTHER, 'Other'),
)

FREQ_CHOICES = (
    (QDAY, 'Once daily'),
    (BID, 'Twice daily'),
    (TID, 'Three times daily'),
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
    (Decimal("0.6"), '0.6 mg'),
    (Decimal("1.2"), '1.2 mg'),
)

PREDNISONE_DOSE_CHOICES = (
    (5, '5 mg'),
    (10, '10 mg'),
    (15, '15 mg'),
    (20, '20 mg'),
    (30, '30 mg'),
    (40, '40 mg'),
    (60, '60 mg'),
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

INDOMETHACIN_DOSE_CHOICES = (
    (25, '25 mg'),
    (50, '50 mg'),
)

NAPROXEN_DOSE_CHOICES = (
    (220, '220 mg'),
    (250, '250 mg'),
    (440, '440 mg'),
    (500, '500 mg'),
)

MELOXICAM_DOSE_CHOICES = (
    (Decimal("7.5"), '7.5 mg'),
    (Decimal("15"), '15 mg'),
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
    ('None', 'None'),
)

FEBUXOSTAT_SIDE_EFFECT_CHOICES = (
    ('Rash', 'Rash'),
    ('Hypersensitivity syndrome', 'Hypersensitivity syndrome'),
    ('Elevated LFTs', 'Elevated LFTs'),
    ('Cytopenias', 'Cytopenias'),
    ('GI upset', 'GI upset'),
    ('None', 'None'),
)

COLCHICINE_SIDE_EFFECT_CHOICES = (
    ('GI upset', 'GI upset'),
    ('Medication interaction', 'Medication interaction'),
    ('None', 'None'),
)

NSAID_SIDE_EFFECT_CHOICES = (
    ('Rash', 'Rash'),
    ('Kidney failure', 'Kidney failure'),
    ('Stomach ulcer', 'Stomach ulcer'),
    ('GI upset', 'GI upset'),
    ('Medication interaction', 'Medication interaction'),
    ('None', 'None'),
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
    ('None', 'None'),
)

INJECTION_SIDE_EFFECT_CHOICES = (
    ('Bleeding', 'Bleeding'),
    ('Infection', 'Infection'),
    ('None', 'None'),
)

PROBENECID_SIDE_EFFECT_CHOICES = (
    ('Flushing', 'Flushing'),
    ('Headache', 'Headache'),
    ('None', 'None'),
)
