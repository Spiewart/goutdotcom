from autoslug import AutoSlugField
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
from django_extensions.db.models import TimeStampedModel
from django.urls import reverse

from ..treatment.models import Allopurinol, Colchicine, Febuxostat, Ibuprofen, Celecoxib, Meloxicam, Naproxen, Prednisone, Probenecid, Methylprednisolone

TOER1 = 'Right great toe'
TOER2 = 'Right second toe'
TOER3 = 'Right third toe'
TOER4 = 'Right fourth toe'
TOER5 = 'Right little toe'
TOEL1 = 'Left great toe'
TOEL2 = 'Left secont toe'
TOEL3 = 'Left third toe'
TOEL4 = 'Left fourth toe'
TOEL5 = 'Left little toe'
ANKLER = 'Right ankle'
ANKLEL = 'Left ankle'
KNEER = 'Right knee'
KNEEL = 'Left knee'
HIPR = 'Right hip'
HIPL = 'Left hip'
FINGR1 = 'Right thumb'
FINGR2 = 'Right index finger'
FINGR3 = 'Right middle finger'
FINGR4 = 'Right ring finger'
FINGR5 = 'Right little finger'
FINGL1 = 'Left thumb'
FINGL2 = 'Left index finger'
FINGL3 = 'Left middle finger'
FINGL4 = 'Left ring finger'
FINGL5 = 'Left little finger'
WRISTR = 'Right wrist'
WRISTL = 'Left wrist'
ELBOWR = 'Right elbow'
ELBOWL = 'Left elbow'
SHOUDLERR = 'Right shoulder'
SHOULDERL = 'Left shoulder'

JOINT_CHOICES = (
    (TOER1, 'Right great toe'),
    (TOER2, 'Right second toe'),
    (TOER3, 'Right third toe'),
    (TOER4, 'Right fourth toe'),
    (TOER5, 'Right little toe'),
    (TOEL1, 'Left great toe'),
    (TOEL2, 'Left secont toe'),
    (TOEL3, 'Left third toe'),
    (TOEL4, 'Left fourth toe'),
    (TOEL5, 'Left little toe'),
    (ANKLER, 'Right ankle'),
    (ANKLEL, 'Left ankle'),
    (KNEER, 'Right knee'),
    (KNEEL, 'Left knee'),
    (HIPR, 'Right hip'),
    (HIPL,'Left hip'),
    (FINGR1, 'Right thumb'),
    (FINGR2, 'Right index finger'),
    (FINGR3, 'Right middle finger'),
    (FINGR4, 'Right ring finger'),
    (FINGR5, 'Right little finger'),
    (FINGL1, 'Left thumb'),
    (FINGL2, 'Left index finger'),
    (FINGL3, 'Left middle finger'),
    (FINGL4, 'Left ring finger'),
    (FINGL5, 'Left little finger'),
    (WRISTR, 'Right wrist'),
    (WRISTL, 'Left wrist'),
    (ELBOWR, 'Right elbow'),
    (ELBOWL, 'Left elbow'),
    (SHOUDLERR, 'Right shoulder'),
    (SHOULDERL, 'Left shoulder'),
)

TREATMENT_CHOICES = (
    (Allopurinol, 'Allopurinol'),
    (Febuxostat, 'Febuxostat'),
    (Colchicine, 'Colchicine'),
    (Ibuprofen, 'Ibuprofen'),
)

class Flare(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    slug = AutoSlugField(
            "Flare Detail", unique=True, always_update=False, populate_from="created_at"
        )

    location = models.CharField(max_length=60, choices=JOINT_CHOICES, blank=True,
                                help_text="What joint did the flare occur in?")

    treatement = models.ForeignKey(TREATMENT_CHOICES, max_length=50, choices=TREATMENT_CHOICES,
                                   help_text="What was the flare treated with?", on_delete=models.CASCADE)

    duration = models.IntegerField(help_text="How long did it last? (days)")
    urate = models.OneToOneField('Urate', on_delete=models.CASCADE, help_text="What was the uric acid at the time of the flare?", blank=True, null=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{(str(self.date), str(self.user), str(self.location))}'

    def get_absolute_url(self):
        return reverse('flare:detail', args=[str(self.created)])
