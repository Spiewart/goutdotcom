from autoslug import AutoSlugField
from django.db import models
from django.conf import settings
from django_extensions.db.models import TimeStampedModel
from django.urls import reverse

from ..lab.models import Urate
from ..treatment.models import Colchicine, Ibuprofen, Celecoxib, Meloxicam, Naproxen, Prednisone,  Methylprednisolone

TinctureofTime = 'Tincture of time'
Other = 'Other'
Colcrys = 'Colcrys'
Advil = 'Advil'
Aleve = 'Aleve'
Celebrex = 'Celebrex'
Mobic = 'Mobic'
Pred = 'Pred'
Methylpred = 'Methylpred'

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
    (TOEL2, 'Left second toe'),
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
    (Colcrys, 'Colchicine'),
    (Advil, 'Ibuprofen'),
    (Aleve, 'Naproxen'),
    (Celebrex, 'Celecoxib'),
    (Mobic, 'Meloxicam'),
    (Pred, 'Prednisone'),
    (Methylpred, 'Methylprednisolone'),
    (TinctureofTime, 'Tincture of time'),
    (Other, 'Other'),
)

BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))

NO = "No"
LOGGED = "Already logged it"
TOLOG = "Will log it now"

LOG_CHOICES = ((NO, 'No'), (LOGGED, 'Already logged it'), (TOLOG, 'Will log it now'))

class Flare(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    location = models.CharField(max_length=60, choices=JOINT_CHOICES, blank=True,
                                help_text="What joint did the flare occur in?")


    treatment = models.CharField(max_length=60, choices=TREATMENT_CHOICES,
                                   help_text="What was the flare treated with?")
    treatment_log = models.CharField(max_length=60, choices=LOG_CHOICES, help_text="Do you want to or have you already logged you treatment?")
    
    colchicine = models.OneToOneField(Colchicine, null=True, blank=True, on_delete=models.CASCADE)
    ibuprofen = models.OneToOneField(Ibuprofen, null=True, blank=True, on_delete=models.CASCADE)
    naproxen = models.OneToOneField(Naproxen, null=True, blank=True, on_delete=models.CASCADE)
    celecoxib = models.OneToOneField(Celecoxib, null=True, blank=True, on_delete=models.CASCADE)
    meloxicam = models.OneToOneField(Meloxicam, null=True, blank=True, on_delete=models.CASCADE)
    prednisone = models.OneToOneField(Prednisone, null=True, blank=True, on_delete=models.CASCADE)
    methylprednisolone = models.OneToOneField(Methylprednisolone, null=True, blank=True, on_delete=models.CASCADE)

    duration = models.IntegerField(help_text="How long did it last? (days)")
    
    urate_draw = models.BooleanField(choices=BOOL_CHOICES, help_text="Did you get your uric acid checked during your flare?", default=False)
    urate_log = models.CharField(max_length=60, choices=LOG_CHOICES, help_text="Do you want to log or have you already logged your uric acid?")
    urate = models.OneToOneField(Urate, on_delete=models.CASCADE, help_text="What was the uric acid at the time of the flare?", blank=True, null=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'{(str(self.user), str(self.location))}'

    def get_absolute_url(self):
        return reverse('flare:detail', kwargs={"pk":self.pk})
        
