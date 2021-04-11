from django.db import models
from django_extensions.db.models import TimeStampedModel

# Create your models here.
class ULT(TimeStampedModel):
    ZERO = 'zero'
    ONE = 'one'
    FEW = '1-3'
    LOTS = '4-6'
    CONSTANT = '7 or more'

    UNDER_TWO = 'Under two'
    GREATER_TWO = 'Greater than two'

    ULT_CHOICES = (
        (ZERO, 'Zero'),
        (ONE, 'One'),
        (FEW, '1-3'),
        (LOTS, '4-6'),
        (CONSTANT, '7 or more'),
    )

    FREQ_CHOICES = (
        (UNDER_TWO, 'Under two'),
        (GREATER_TWO, 'Greater than two'),
    )

    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))

    num_flares = models.CharField(max_length=30, choices=ULT_CHOICES, help_text="Approximately how many gout flares have you had?")
    freq_flares = models.CharField(max_length=30, choices=FREQ_CHOICES, help_text="Approximately how often do you have flares?")
    first_flare = models.BooleanField(choices=BOOL_CHOICES, help_text="Is this your first flare?")
    erosions = models.BooleanField(choices=BOOL_CHOICES, help_text="Do you have erosions on your x-rays? If you don't know, that's OK!")
    tophi = models.BooleanField(choices=BOOL_CHOICES, help_text="Do you have tophi? If you don't know, that's OK!")
    stones = models.BooleanField(choices=BOOL_CHOICES, help_text="Have you ever had kidney stones made of uric acid? If you don't know, that's OK!")
    ckd = models.BooleanField(choices=BOOL_CHOICES, help_text="Do you have chronic kidney disease (CKD)? If you don't know, that's OK!")
    uric_acid = models.BooleanField(choices=BOOL_CHOICES, help_text="Is your uric acid over 9.0? If you don't know, that's OK!")

    def calculator(self):
        go_forth = "Urate lowering therapy is recommended for your gout."
        abstain = "Urate lowering therapy isn't indicated for your gout."
        conditional = "Urate lowering therapy is conditionally recommended for your gout."

        if self.first_flare == True:
            return abstain
        elif self.erosions == True:
            return go_forth
        elif self.tophi == True:
            return go_forth
        elif self.num_flares != "Zero" or "One":
            return abstain
        elif self.num_flares == "One" & self.freq_flares == "Greater than two":
            return go_forth
        elif self.ckd == True or self.stones == True or self.uric_acid == True:
            return conditional
        else:
            return abstain

    def __str__(self):
        return self.calculator()

